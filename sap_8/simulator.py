from enum import Enum
import argparse
import time
import microcode
import rom


class Control(Enum):
    Xc = 1
    Tr = 2
    Pr = 3
    Ps = 4
    Io = 5
    Oi = 6
    Bo = 7
    Bi = 8
    Lo = 9
    Ls = 10
    Ao = 11
    Ai = 12
    Co = 13
    Ci = 14
    So = 15
    Ri = 16
    Ro = 17
    Mi = 18
    Pi = 19
    Po = 20
    Pc = 21
    Ch = 22


opcodes = {
    0x00: 'NOP',
    0x01: 'HLT',
    0x02: 'LDI',
    0x03: 'LDA',
    0x04: 'STA',
    0x05: 'STM',
    0x06: 'ADI',
    0x07: 'ADD',
    0x08: 'SUI',
    0x09: 'SUB',
    0x0A: 'CMI',
    0x0B: 'CMP',
    0x10: 'JMP',
    0x11: 'JC',
    0x12: 'JZ',
    0x13: 'JNZ',
    0x14: 'PAGE0',
    0x15: 'PAGE1',
    0x16: 'RESET',
    0x18: 'OUTA',
    0x19: 'OUTB',
    0x1A: 'OUTC',
    0x1B: 'OUTD',
    0x1C: 'OUTE',
    0x1D: 'OUTF',
    0x1E: 'INA',
    0x1F: 'INB'
}


def opcode_to_instruction(opcode):
    if opcode in opcodes.keys():
        return opcodes[opcode]
    else:
        return 'ERR'


rom = rom.data


def build_rom(_bytecode):
    bytes_array = list(_bytecode)
    for i, byte in enumerate(bytes_array):
        rom[i] = byte


class State:
    def __init__(self, _rom, _ram, verbose):
        if _rom is not None:
            build_rom(_rom)

        if _ram is not None:
            self.build_memory(_ram)
        self.verbose = verbose

    clock: bool = False
    verbose: bool = False

    bus: int = 0
    memory: list[int] = [0] * 256
    control_word: int = 0
    control_active_bits: list[Control] = []
    t_state: int = 0

    pc: int = 0
    mar: int = 0
    ir: int = 0
    alu: int = 0
    flags: int = 0
    page: int = 0
    reg_a: int = 0
    reg_b: int = 0
    out_a: int = 0
    out_b: int = 0
    out_c: int = 0
    out_d: int = 0
    out_e: int = 0
    out_f: int = 0
    in_a: int = 0
    in_b: int = 0

    def build_memory(self, _bytecode):
        bytes_array = list(_bytecode)
        for i, byte in enumerate(bytes_array):
            self.memory[i] = byte

    def load_microcode(self):
        self.control_word = microcode.build(self.page, self.flags, self.ir, self.t_state)

    def decode_control_word(self):
        self.control_active_bits.clear()
        for i in range(0, len(Control)):
            if self.control_word & (1 << i) > 0:
                self.control_active_bits.append(Control(i + 1))

    def update(self):
        # Write to bus
        self.bus = 0
        if Control.Lo in self.control_active_bits:
            self.bus = self.alu
        if Control.Ao in self.control_active_bits:
            self.bus = self.reg_a
        if Control.Bo in self.control_active_bits:
            self.bus = self.reg_b
        if Control.Co in self.control_active_bits:
            self.bus = self.ir
        if Control.Ro in self.control_active_bits:
            self.bus = self.memory[self.mar]
        if Control.So in self.control_active_bits:
            self.bus = rom[self.mar]
        if Control.Po in self.control_active_bits:
            self.bus = self.pc
        if Control.Io in self.control_active_bits:
            if self.ir & 7 == 6:
                self.bus = self.in_a
            elif self.ir & 7 == 7:
                self.bus = self.in_b

        # Read from bus
        if self.clock:
            if Control.Oi in self.control_active_bits:
                if self.ir & 7 == 0:
                    self.out_a = self.bus
                elif self.ir & 7 == 1:
                    self.out_b = self.bus
                elif self.ir & 7 == 2:
                    self.out_c = self.bus
                elif self.ir & 7 == 3:
                    self.out_d = self.bus
                elif self.ir & 7 == 4:
                    self.out_e = self.bus
                elif self.ir & 7 == 5:
                    self.out_f = self.bus
                self.out_a = self.bus
            if Control.Bi in self.control_active_bits:
                self.reg_b = self.bus
            if Control.Ai in self.control_active_bits:
                self.reg_a = self.bus
            if Control.Ci in self.control_active_bits:
                self.ir = self.bus
            if Control.Mi in self.control_active_bits:
                self.mar = self.bus
            if Control.Ri in self.control_active_bits:
                self.memory[self.mar] = self.bus
            if Control.Pi in self.control_active_bits:
                self.pc = self.bus
            if Control.Ps in self.control_active_bits:
                self.page = 1
            if Control.Pr in self.control_active_bits:
                self.page = 0

        # Update ALU
        self.flags = 0
        if Control.Ls in self.control_active_bits:
            alu_sum = self.reg_a - self.reg_b
            if alu_sum == 0:
                self.flags += 1
            elif alu_sum > 255:
                self.flags += 2
            self.alu = alu_sum % 256
        else:
            alu_sum = self.reg_a + self.reg_b
            if alu_sum == 0:
                self.flags += 1
            elif alu_sum > 255:
                self.flags += 2
            self.alu = alu_sum % 256

        # Update pc
        if self.clock and Control.Pc in self.control_active_bits:
            self.pc = (self.pc + 1) % 256

    def print(self):
        print("c/t %d/%d | bus %02X | " % (self.clock, self.t_state, self.bus), end='')
        print(
            "pc %02X | mar %02X | mem %02X | ir %02X | alu %02X | Ra %02X | Rb %02X | out %02X:%02X:%02X:%02X:%02X:%02X | in %02X:%02X | " %
            (self.pc, self.mar, self.memory[self.mar] if self.page == 1 else rom[self.mar], self.ir, self.alu, self.reg_a, self.reg_b, self.out_a, self.out_b, self.out_c, self.out_d, self.out_e, self.out_f, self.in_a, self.in_b),
            end=''
        )
        print(
            "f %s | p %d | asm %s | ctrl [%s]" %
            (f'{self.flags:02b}', self.page, f'{opcode_to_instruction(self.ir):<5}', ', '.join([d.name for d in self.control_active_bits]))
        )

    def step_clock(self):
        # Is this t-state implementation correct?
        if Control.Ch not in self.control_active_bits:
            time.sleep(0.0001)
            self.clock = not self.clock
            if not self.clock:
                if Control.Tr in self.control_active_bits:
                    self.t_state = 0
                else:
                    self.t_state = (self.t_state + 1) % 7
            self.load_microcode()
            self.decode_control_word()
            self.update()
            if self.clock or self.verbose:
                self.print()


def run(_rom_bytecode, _ram_bytecode, verbose):
    state = State(_rom_bytecode, _ram_bytecode, verbose)
    while Control.Ch not in state.control_active_bits:
        state.step_clock()


def load_file(file_path):
    with open(file_path, "rb") as file_path:
        file = file_path.read()
        return file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='sap_8_extended_simulator',
        description='SAP-8 Simulator',
    )
    parser.add_argument('-r', '--rom', type=str, default=None, help='Input ROM bytecode file')
    parser.add_argument('-m', '--ram', type=str, default=None, help='Input RAM bytecode file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print each time the clock flips')

    args = parser.parse_args()

    rom_bytecode = None
    ram_bytecode = None

    if args.rom:
        rom_bytecode = load_file(args.rom)
    elif args.ram:
        ram_bytecode = load_file(args.rom)

    run(rom_bytecode, ram_bytecode, args.verbose)

