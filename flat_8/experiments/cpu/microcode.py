Ch = 0b10000000000000000000000000000000    # halt clock
Cp = 0b01000000000000000000000000000000    # increment program counter
Ep = 0b00100000000000000000000000000000    # program counter out
Lp = 0b00010000000000000000000000000000    # program counter in
Lm = 0b00001000000000000000000000000000    # memory address register in
Er = 0b00000100000000000000000000000000    # memory out
Lr = 0b00000010000000000000000000000000    # memory in
Li = 0b00000001000000000000000000000000    # instruction register in
Ei = 0b00000000100000000000000000000000    # instruction register out
La = 0b00000000010000000000000000000000    # accumulator in
Ea = 0b00000000001000000000000000000000    # accumulator out
Lb = 0b00000000000100000000000000000000    # b register in
Eb = 0b00000000000010000000000000000000    # b register out
Lc = 0b00000000000001000000000000000000    # c register in
Ec = 0b00000000000000100000000000000000    # c register out
Lx = 0b00000000000000010000000000000000    # alu temporary x register in
Ly = 0b00000000000000001000000000000000    # alu temporary y register in
Us = 0b00000000000000000100000000000000    # alu subtract mode
Ua = 0b00000000000000000010000000000000    # alu and mode
Uo = 0b00000000000000000001000000000000    # alu or mode
Ux = 0b00000000000000000000100000000000    # alu xor mode
Eu = 0b00000000000000000000010000000000    # alu out
Ef = 0b00000000000000000000001000000000    # flags register out
Lf = 0b00000000000000000000000100000000    # flags register in
I0 = 0b00000000000000000000000010000000    # IO register 0 in
I1 = 0b00000000000000000000000001000000    # IO register 1 in
O0 = 0b00000000000000000000000000100000    # IO register 2 in
O1 = 0b00000000000000000000000000010000    # IO register 3 in
O2 = 0b00000000000000000000000000001000    # IO register 4 in
O3 = 0b00000000000000000000000000000100    # IO register 5 in
O4 = 0b00000000000000000000000000000010    # IO register 6 in
O5 = 0b00000000000000000000000000000001    # IO register 7 in

matrix = [
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 00000000 NOP
    [Ep | Lm, Cp, Er | Li, Ei | Lm, Er | La, 0],                # 00000001 LDA
    [Ep | Lm, Cp, Er | Li, Lm | Ei, Er | Lb, La | Eu],          # 00000010 ADD
    [Ep | Lm, Cp, Er | Li, Lm | Ei, Er | Lb, La | Eu | Us],     # 00000011 SUB
    [Ep | Lm, Cp, Er | Li, Ea | O0, 0, 0],                      # 00000100 OUT
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],
    [Ep | Lm, Cp, Er | Li, Ch, 0, 0]                             # 00001111 HLT
]
