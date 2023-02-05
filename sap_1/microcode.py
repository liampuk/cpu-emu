Ch = 0b1000000000000    # halt clock
Cp = 0b0100000000000    # increment program counter
Ep = 0b0010000000000    # enable program counter
Lm = 0b0001000000000    # memory address register in
CE = 0b0000100000000    # memory out
Li = 0b0000010000000    # instruction register in
Ei = 0b0000001000000    # instruction register out
La = 0b0000000100000    # accumulator in
Ea = 0b0000000010000    # accumulator out
Su = 0b0000000001000    # alu subtract mode
Eu = 0b0000000000100    # alu out
Lb = 0b0000000000010    # b register in
Lo = 0b0000000000001    # output register in

matrix = [
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],                            # 0000 NOP
    [Ep | Lm, Cp, CE | Li, Ei | Lm, CE | La, 0],                # 0001 LDA
    [Ep | Lm, Cp, CE | Li, Lm | Ei, CE | Lb, La | Eu],          # 0010 ADD
    [Ep | Lm, Cp, CE | Li, Lm | Ei, CE | Lb, La | Eu | Su],     # 0011 SUB
    [Ep | Lm, Cp, CE | Li, Ea | Lo, 0, 0],                      # 0100 OUT
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, 0, 0, 0],
    [Ep | Lm, Cp, CE | Li, Ch, 0, 0]                             # 1111 HLT
]
