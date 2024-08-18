# Control word

Ch = 0b100000000000000      # halt clock
Cp = 0b010000000000000      # increment program counter
Ep = 0b001000000000000      # program counter out
Lp = 0b000100000000000      # program counter in
Lm = 0b000010000000000      # memory address register in
Ro = 0b000001000000000      # memory out
Ri = 0b000000100000000      # memory in
Li = 0b000000010000000      # instruction register in
Ei = 0b000000001000000      # instruction register out
La = 0b000000000100000      # accumulator in
Ea = 0b000000000010000      # accumulator out
Su = 0b000000000001000      # alu subtract mode
Eu = 0b000000000000100      # alu out
Lb = 0b000000000000010      # b register in
Lo = 0b000000000000001      # output register in

# Flag dependant instruction indexes

JC = 8
JZ = 9
JNZ = 10

# Instruction matrix

matrix = [
    [Ep | Lm, Cp | Ro | Li, 0, 0, 0],                            # 0000 NOP
    [Ep | Lm, Cp | Ro | Li, Ei | Lm, Ro | La, 0],                # 0001 LDA
    [Ep | Lm, Cp | Ro | Li, Lm | Ei, Ro | Lb, La | Eu],          # 0010 ADD
    [Ep | Lm, Cp | Ro | Li, Lm | Ei, Ro | Lb, La | Eu | Su],     # 0011 SUB
    [Ep | Lm, Cp | Ro | Li, Ea | Lo, 0, 0],                      # 0100 OUT
    [Ep | Lm, Cp | Ro | Li, Ei | Lm, Ri | Ea, 0],                # 0101 STA
    [Ep | Lm, Cp | Ro | Li, Ei | La, 0, 0],                      # 0110 LDI
    [Ep | Lm, Cp | Ro | Li, Ei | Lp, 0, 0],                      # 0111 JMP
    [0, 0, 0, 0, 0],                                         # 1000 JC
    [0, 0, 0, 0, 0],                                         # 1001 JZ
    [0, 0, 0, 0, 0],                                         # 1010 JNZ
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [Ep | Lm, Cp | Ro | Li, Ch, 0, 0]                             # 1111 HLT
]

# Flag dependent instruction matrices [C, Z]

jc_flags = [
    [Ep | Lm, Cp | Ro | Li, 0, 0, 0],
    [Ep | Lm, Cp | Ro | Li, 0, 0, 0],
    [Ep | Lm, Cp | Ro | Li, Ei | Lp, 0, 0],
    [Ep | Lm, Cp | Ro | Li, Ei | Lp, 0, 0]
]

jz_flags = [
    [Ep | Lm, Cp | Ro | Li, 0, 0, 0],
    [Ep | Lm, Cp | Ro | Li, Ei | Lp, 0, 0],
    [Ep | Lm, Cp | Ro | Li, 0, 0, 0],
    [Ep | Lm, Cp | Ro | Li, Ei | Lp, 0, 0],
]

jnz_flags = [
    [Ep | Lm, Cp | Ro | Li, Ei | Lp, 0, 0],
    [Ep | Lm, Cp | Ro | Li, 0, 0, 0],
    [Ep | Lm, Cp | Ro | Li, Ei | Lp, 0, 0],
    [Ep | Lm, Cp | Ro | Li, 0, 0, 0],
]


def build(flags, program_count, step):
    matrix[JC] = jc_flags[flags]
    matrix[JZ] = jz_flags[flags]
    matrix[JNZ] = jnz_flags[flags]
    return matrix[program_count][step]