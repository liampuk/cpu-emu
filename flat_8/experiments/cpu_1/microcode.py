Ch = 0b10000000000000000000000000000000000000    # halt clock
Cp = 0b01000000000000000000000000000000000000    # increment program counter
Ep = 0b00100000000000000000000000000000000000    # program counter out
Lp = 0b00010000000000000000000000000000000000    # program counter in
Lm = 0b00001000000000000000000000000000000000    # memory address register in
Er = 0b00000100000000000000000000000000000000    # memory out
Lr = 0b00000010000000000000000000000000000000    # memory in
Li = 0b00000001000000000000000000000000000000    # instruction register in
Ei = 0b00000000100000000000000000000000000000    # instruction register out
La = 0b00000000010000000000000000000000000000    # accumulator in
Ea = 0b00000000001000000000000000000000000000    # accumulator out
Lb = 0b00000000000100000000000000000000000000    # b register in
Eb = 0b00000000000010000000000000000000000000    # b register out
Lc = 0b00000000000001000000000000000000000000    # c register in
Ec = 0b00000000000000100000000000000000000000    # c register out
Lx = 0b00000000000000010000000000000000000000    # alu temporary x register in
Ly = 0b00000000000000001000000000000000000000    # alu temporary y register in
Us = 0b00000000000000000100000000000000000000    # alu subtract mode
Ua = 0b00000000000000000010000000000000000000    # alu and mode
Uo = 0b00000000000000000001000000000000000000    # alu or mode
Ux = 0b00000000000000000000100000000000000000    # alu xor mode
Uf = 0b00000000000000000000010000000000000000    # alu flags out
Eu = 0b00000000000000000000001000000000000000    # alu out
Ef = 0b00000000000000000000000100000000000000    # flags register out
Lf = 0b00000000000000000000000010000000000000    # flags register in
I0 = 0b00000000000000000000000001000000000000    # input register 0 in
I1 = 0b00000000000000000000000000100000000000    # input register 1 in
O0 = 0b00000000000000000000000000010000000000    # input register 0 out
O1 = 0b00000000000000000000000000001000000000    # input register 1 out
O2 = 0b00000000000000000000000000000100000000    # input register 2 out
O3 = 0b00000000000000000000000000000010000000    # input register 3 out
O4 = 0b00000000000000000000000000000001000000    # input register 4 out
P0 = 0b00000000000000000000000000000000100000    # set page flag to 0
P1 = 0b00000000000000000000000000000000010000    # set page flag to 1
Ie = 0b00000000000000000000000000000000001000    # enable interrupts
Id = 0b00000000000000000000000000000000000100    # disable interrupts
Rr = 0b00000000000000000000000000000000000010    # reset registers
Rt = 0b00000000000000000000000000000000000001    # reset t-state counter

matrix = [
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 000 NOP
    [Ep | Lm, Cp, Er | Li, Ei | Lm, Er | La, 0],                # 001 MOV A, I
    [Ep | Lm, Cp, Er | Li, Lm | Ei, Er | Lb, La | Eu],          # 002 MOV B, I
    [Ep | Lm, Cp, Er | Li, Lm | Ei, Er | Lb, La | Eu | Us],     # 003 MOV C, I
    [Ep | Lm, Cp, Er | Li, Ea | O0, 0, 0],                      # 004 LDI A, [I]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 005 LDI B, [I]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 006 LDI C, [I]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 007 LDR A, [B]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 008 LDR A, [C]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 009 LDR B, [A]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 010 LDR B, [C]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 011 LDR C, [A]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 012 LDR C, [B]
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 013 STI [I], A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 014 STI [I], B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 015 STI [I], C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 016 STR [A], B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 017 STR [A], C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 018 STR [B], A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 019 STR [B], C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 020 STR [C], A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 021 STR [C], B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 022 ADD A, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 023 ADD A, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 024 ADD B, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 025 ADD B, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 026 ADD C, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 027 ADD C, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 028 ADD A, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 029 ADD B, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 030 ADD C, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 031 SUB A, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 032 SUB A, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 033 SUB B, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 034 SUB B, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 035 SUB C, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 036 SUB C, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 037 SUB A, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 038 SUB B, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 039 SUB C, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 040 AND A, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 041 AND A, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 042 AND B, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 043 AND B, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 044 AND C, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 045 AND C, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 046 AND A, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 047 AND B, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 048 AND C, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 049 OR A, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 050 OR A, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 051 OR B, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 052 OR B, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 053 OR C, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 054 OR C, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 055 OR A, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 056 OR B, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 057 OR C, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 058 XOR A, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 059 XOR A, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 060 XOR B, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 061 XOR B, C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 062 XOR C, A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 063 XOR C, B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 064 XOR A, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 065 XOR B, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 066 XOR C, I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 067 JMP I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 068 JZ I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 069 JNZ I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 070 JS I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 071 JNS I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 072 JC I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 073 JNC I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 074 CALL I
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 075 RET
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 076 IRET
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 077 PUSH A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 078 PUSH B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 079 PUSH C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 080 POP A
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 081 POP B
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 082 POP C
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 083 PUSHF
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 084 POPF
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 085 IN 0
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 086 IN 1
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 087 OUT 0
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 088 OUT 1
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 089 OUT 2
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 090 OUT 3
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 091 OUT 4
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 092 STI
    [Ep | Lm, Cp, Er | Li, 0, 0, 0],                            # 093 CLI

    [Ep | Lm, Cp, Er | Li, Ch, 0, 0]                            # 255 HLT
]
