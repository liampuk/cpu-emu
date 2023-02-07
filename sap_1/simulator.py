from enum import Enum
import microcode


class Control(Enum):
    Ch = 13
    Cp = 12
    Ep = 11
    Lm = 10
    CE = 9
    Li = 8
    Ei = 7
    La = 6
    Ea = 5
    Su = 4
    Eu = 3
    Lb = 2
    Lo = 1


class State:
    clock: bool = False

    bus: int = 0
    memory: list[int] = [0] * 16
    control_word: int = 0
    control_active_bits: list[Control] = []
    t_state: int = 0

    pc: int = 0
    mar: int = 0
    ir: int = 0
    alu: int = 0
    reg_a: int = 0
    reg_b: int = 0
    out: int = 0

    # Build Memory

    memory[0] = 0b00010101      # LDA [05]
    memory[1] = 0b00100110      # ADD [05]
    memory[2] = 0b00110111      # SUB [06]
    memory[3] = 0b01000000      # OUT
    memory[4] = 0b11110000      # HLT
    memory[5] = 0b00000100
    memory[6] = 0b00000010
    memory[7] = 0b00000001

    # End Build Memory

    def load_microcode(self):
        self.control_word = microcode.matrix[(self.ir & 240) >> 4][self.t_state]

    def decode_control_word(self):
        self.control_active_bits.clear()
        for i in range(0, 13):
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
        if Control.CE in self.control_active_bits:
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

        # Update ALU
        if Control.Su in self.control_active_bits:
            self.alu = self.reg_a - self.reg_b
        else:
            self.alu = self.reg_a + self.reg_b

        # Update pc
        if self.clock and Control.Cp in self.control_active_bits:
            self.pc = (self.pc + 1) % 16

    def print(self):
        print("bus %s | clk %d | t_state %d | " % (f'{self.bus:08b}', self.clock, self.t_state), end='')
        print(
            "pc %d | mar %d | ir %s | alu %d | reg_a %d | reg_b  %d | out %d | " %
            (self.pc, self.mar, f'{self.ir:08b}', self.alu, self.reg_a, self.reg_b, self.out),
            end=''
        )
        print(
            "control word %s | control active %s" %
            (f'{self.control_word:012b}', [d.name for d in self.control_active_bits])
        )

    def step_clock(self):
        if Control.Ch not in self.control_active_bits:
            self.clock = not self.clock
            if not self.clock:
                self.t_state = (self.t_state + 1) % 6
            self.load_microcode()
            self.decode_control_word()
            self.update()
            if self.clock:
                self.print()


def run():
    state = State()
    for i in range(1, 100):
        state.step_clock()


if __name__ == '__main__':
    run()
