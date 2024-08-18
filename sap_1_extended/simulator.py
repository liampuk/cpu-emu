import math
from enum import Enum
import argparse
import time
import assembler
import microcode


class Control(Enum):
    Ch = 15
    Cp = 14
    Ep = 13
    Lp = 12
    Lm = 11
    Ro = 10
    Ri = 9
    Li = 8
    Ei = 7
    La = 6
    Ea = 5
    Su = 4
    Eu = 3
    Lb = 2
    Lo = 1


class State:

    def __init__(self, _bytecode, verbose):
        self.build_memory(_bytecode)
        self.verbose = verbose

    clock: bool = False
    verbose: bool = False

    bus: int = 0
    memory: list[int] = [0] * 16
    control_word: int = 0
    control_active_bits: list[Control] = []
    t_state: int = 0

    pc: int = 0
    mar: int = 0
    ir: int = 0
    alu: int = 0
    flags: int = 0
    reg_a: int = 0
    reg_b: int = 0
    out: int = 0

    def build_memory(self, _bytecode):
        bytes_array = list(_bytecode)
        for i, byte in enumerate(bytes_array):
            self.memory[i] = byte

    def load_microcode(self):
        self.control_word = microcode.build(self.flags, (self.ir & 240) >> 4, self.t_state)

    def decode_control_word(self):
        self.control_active_bits.clear()
        for i in range(0, len(Control)):
            if self.control_word & (1 << i) > 0:
                self.control_active_bits.append(Control(i + 1))

    def update(self):
        # Write to bus
        self.bus = 0
        if Control.Eu in self.control_active_bits:
            self.bus = self.alu
        if Control.Ea in self.control_active_bits:
            self.bus = self.reg_a
        if Control.Ei in self.control_active_bits:
            self.bus = self.ir & 15
        if Control.Ro in self.control_active_bits:
            self.bus = self.memory[self.mar]
        if Control.Ep in self.control_active_bits:
            self.bus = self.pc & 15

        # Read from bus
        if self.clock:
            if Control.Lo in self.control_active_bits:
                self.out = self.bus
            if Control.Lb in self.control_active_bits:
                self.reg_b = self.bus
            if Control.La in self.control_active_bits:
                self.reg_a = self.bus
            if Control.Li in self.control_active_bits:
                self.ir = self.bus
            if Control.Lm in self.control_active_bits:
                self.mar = self.bus & 15
            if Control.Ri in self.control_active_bits:
                self.memory[self.mar] = self.bus
            if Control.Lp in self.control_active_bits:
                self.pc = self.bus

        # Update ALU
        self.flags = 0
        if Control.Su in self.control_active_bits:
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
        if self.clock and Control.Cp in self.control_active_bits:
            self.pc = (self.pc + 1) % 16

    def print(self):
        print("bus %s | clk %d | t_state %d | " % (f'{self.bus:08b}', self.clock, self.t_state), end='')
        print(
            "pc %s | mar %s | ir %s | alu %s | reg_a %s | reg_b %s | out %s | " %
            (f'{self.pc:02d}', f'{self.mar:02d}', f'{self.ir:08b}', f'{self.alu:03d}', f'{self.reg_a:03d}', f'{self.reg_b:03d}', f'{self.out:03d}'),
            end=''
        )
        print(
            "control word %s | flags %s | control active %s" %
            (f'{self.control_word:015b}', f'{self.flags:02b}', [d.name for d in self.control_active_bits])
        )

    def step_clock(self):
        if Control.Ch not in self.control_active_bits:
            time.sleep(0.0001)
            self.clock = not self.clock
            if not self.clock:
                self.t_state = (self.t_state + 1) % 5
            self.load_microcode()
            self.decode_control_word()
            self.update()
            if self.clock or self.verbose:
                self.print()


def run(bytecode, verbose):
    state = State(bytecode, verbose)
    while Control.Ch not in state.control_active_bits:
        state.step_clock()


def load_file(file_path):
    with open(file_path, "rb") as file_path:
        file = file_path.read()
        return file


def convert_string_to_bytes(bytes_string):
    num_bytes = math.floor(len(bytes_string) / 8)
    byte_array = [0] * num_bytes
    for i in range(0, num_bytes):
        byte_array[i] = int(bytes_string[i * 8:i * 8 + 8], 2)
    return bytearray(byte_array)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='sap_1_extended_simulator',
        description='SAP-1 Extended Simulator',
    )
    parser.add_argument('-f', '--bytecode-file', type=str, default=None, help='Input bytecode file')
    parser.add_argument('-b', '--bytecode', type=str, default=None, help='Input bytecode')
    parser.add_argument('-a', '--assembly-file', type=str, default=None, help='Input assembly file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print each time the clock flips')

    args = parser.parse_args()

    if args.bytecode:
        run(convert_string_to_bytes(args.bytecode), args.verbose)
    elif args.bytecode_file:
        output = load_file(args.bytecode_file)
        run(output, args.verbose)
    elif args.assembly_file:
        input_bytes = assembler.assemble(args.assembly_file)
        run(input_bytes, args.verbose)
    else:
        print("no bytecode specified")
