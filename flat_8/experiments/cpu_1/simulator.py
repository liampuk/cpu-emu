import math
from enum import Enum
import argparse
import time
import microcode


class Control(Enum):
    Ch = 32
    Cp = 31
    Ep = 30
    Lp = 29
    Lm = 28
    Er = 27
    Lr = 26
    Li = 25
    Ei = 24
    La = 23
    Ea = 22
    Lb = 21
    Eb = 20
    Lc = 19
    Ec = 18
    Lx = 17
    Ly = 16
    Us = 15
    Ua = 14
    Uo = 13
    Ux = 12
    Uf = 11
    Eu = 10
    Ef = 9
    Lf = 8
    I0 = 7
    I1 = 6
    O0 = 5
    O1 = 4
    O2 = 3
    O3 = 2
    O4 = 1

class State:

    def __init__(self, _bytecode, verbose):
        self.build_memory(_bytecode)
        self.verbose = verbose

    clock: bool = False
    verbose: bool = False

    bus: int = 0
    memory: list[int] = [0] * 256
    control_word: int = 0
    control_active_bits: list[Control] = []
    t_state: int = 0
    interrupt: bool = False

    pc: int = 0
    mar: int = 0
    ir: int = 0
    alu: int = 0
    reg_a: int = 0
    reg_b: int = 0
    reg_c: int = 0
    alu_x: int = 0
    alu_y: int = 0
    in_0: int = 0
    in_1: int = 0
    out_0: int = 0
    out_1: int = 0
    out_2: int = 0
    out_3: int = 0
    out_4: int = 0
    stack: int = 0
    # PISCZ
    flags: int = 0

    def build_memory(self, _bytecode):
        bytes_array = list(_bytecode)
        for i, byte in enumerate(bytes_array):
            self.memory[i] = byte

    def load_microcode(self):
        self.control_word = microcode.matrix[self.ir][self.t_state]

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
            self.bus = self.ir
        if Control.Er in self.control_active_bits:
            self.bus = self.memory[self.mar]
        if Control.Ep in self.control_active_bits:
            self.bus = self.pc
        if Control.Eb in self.control_active_bits:
            self.bus = self.reg_b
        if Control.Ec in self.control_active_bits:
            self.bus = self.reg_c
        if Control.Ef in self.control_active_bits:
            self.bus = self.flags
        if Control.I0 in self.control_active_bits:
            self.bus = self.in_0
        if Control.I1 in self.control_active_bits:
            self.bus = self.in_1

        # Read from bus
        if self.clock:
            if Control.Lb in self.control_active_bits:
                self.reg_b = self.bus
            if Control.La in self.control_active_bits:
                self.reg_a = self.bus
            if Control.Li in self.control_active_bits:
                self.ir = self.bus
            if Control.Lm in self.control_active_bits:
                self.mar = self.bus
            if Control.Lr in self.control_active_bits:
                self.memory[self.mar] = self.bus
            if Control.Lp in self.control_active_bits:
                self.pc = self.bus
            if Control.Lb in self.control_active_bits:
                self.reg_b = self.bus
            if Control.Lc in self.control_active_bits:
                self.reg_c = self.bus
            if Control.Lx in self.control_active_bits:
                self.alu_x = self.bus
            if Control.Ly in self.control_active_bits:
                self.alu_y = self.bus
            if Control.Lf in self.control_active_bits:
                self.flags = self.bus & 15
            if Control.O0 in self.control_active_bits:
                self.out_0 = self.bus
            if Control.O1 in self.control_active_bits:
                self.out_1 = self.bus
            if Control.O2 in self.control_active_bits:
                self.out_2 = self.bus
            if Control.O3 in self.control_active_bits:
                self.out_3 = self.bus
            if Control.O4 in self.control_active_bits:
                self.out_4 = self.bus

        # Update ALU
        if Control.Us in self.control_active_bits:
            alu_sum = self.alu_x - self.alu_y
        elif Control.Ua in self.control_active_bits:
            alu_sum = self.alu_x & self.alu_y
        elif Control.Uo in self.control_active_bits:
            alu_sum = self.alu_x | self.alu_y
        elif Control.Ux in self.control_active_bits:
            alu_sum = self.alu_x ^ self.alu_y
        else:
            alu_sum = self.reg_a + self.reg_b

        # Update Flags
        if Control.Uf in self.control_active_bits:
            self.flags = self.flags & 24
            if alu_sum == 0:
                self.flags += 1
            # TODO This is overflow, change to carry
            elif alu_sum > 255:
                self.flags += 2
            # TODO is this how the S flag would work?
            elif alu_sum < 0:
                self.flags += 4

        self.alu = alu_sum % 256

        # Update PC
        if self.clock and Control.Cp in self.control_active_bits:
            self.pc = (self.pc + 1) % 256

    def print(self):
        print("bus %s | t %d | " % (f'{self.bus:08b}', self.t_state), end='')
        print(
            "pc %s | mar %s | ir %s | x %s | y %s | alu %s | " %
            (f'{self.pc:03n}', f'{self.mar:03n}', f'{self.ir:08b}', f'{self.alu_x:03n}', f'{self.alu_y:03n}', f'{self.alu:03n}'),
            end=''
        )
        print(
            "a %s | b %s | c %s | stack %s | o1 %s | " %
            (f'{self.reg_a:03n}', f'{self.reg_b:03n}', f'{self.reg_c:03n}', f'{self.out_0:03n}', f'{self.stack:03n}'),
            end=''
        )
        print(
            "flags %s | control %s" %
            (f'{self.flags:04b}', [d.name for d in self.control_active_bits])
        )

    def step_clock(self):
        if Control.Ch not in self.control_active_bits:
            time.sleep(0.01)
            self.clock = not self.clock
            if not self.clock:
                self.t_state = (self.t_state + 1) % 6
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
        prog='flat_8_simulator',
        description='FLAT-8 Simulator',
    )
    parser.add_argument('-f', '--bytecode-file', type=str, default=None, help='Input bytecode file')
    parser.add_argument('-b', '--bytecode', type=str, default=None, help='Input bytecode')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print each time the clock flips')

    args = parser.parse_args()

    if args.bytecode:
        run(convert_string_to_bytes(args.bytecode), args.verbose)
    elif args.bytecode_file:
        output = load_file(args.bytecode_file)
        run(output, args.verbose)
    else:
        print("no bytecode specified")
