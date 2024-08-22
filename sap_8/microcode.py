# Control word

Ch = 0b1000000000000000000000      # halt clock
Pc = 0b0100000000000000000000      # increment program counter
Po = 0b0010000000000000000000      # program counter out
Pi = 0b0001000000000000000000      # program counter in
Mi = 0b0000100000000000000000      # memory address register in
Ro = 0b0000010000000000000000      # ram out
Ri = 0b0000001000000000000000      # ram in
So = 0b0000000100000000000000      # rom out
Ci = 0b0000000010000000000000      # instruction register in
Co = 0b0000000001000000000000      # instruction register out
Ai = 0b0000000000100000000000      # accumulator in
Ao = 0b0000000000010000000000      # accumulator out
Ls = 0b0000000000001000000000      # alu subtract mode
Lo = 0b0000000000000100000000      # alu out
Bi = 0b0000000000000010000000      # b register in
Bo = 0b0000000000000001000000      # b register in
Oi = 0b0000000000000000100000      # output register in
Io = 0b0000000000000000010000      # input register out
Ps = 0b0000000000000000001000      # set page to 0
Pr = 0b0000000000000000000100      # set page to 1
Tr = 0b0000000000000000000010      # reset t-state
Xc = 0b0000000000000000000001      # reset cpu

# Flag dependant instruction indexes

JC = 17
JZ = 18
JNZ = 19

# Instruction matrix

matrix = [
    [Po | Mi, Pc | Ro | Ci, Tr],                                                            # 00000 NOP
    [Po | Mi, Pc | Ro | Ci, Ch, Tr],                                                        # 00001 HLT
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Ai, Tr],                                     # 00010 LDI
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Bi, Bo | Mi, Ro | Ai, Tr],                   # 00011 LDA
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ao | Ri, Tr],                                     # 00100 STA
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Bi, Bo | Mi, Ao | Ri, Tr],                   # 00101 STM
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Bi, Lo | Ai, Tr],                            # 00110 ADI (immediate)
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Bi, Bo | Mi, Ro | Bi, Lo | Ai],              # 00111 ADD (memory)
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Bi, Ls | Lo | Ai, Tr],                       # 01000 SUI (immediate)
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Bi, Bo | Mi, Ro | Bi, Ls | Lo | Ai],         # 01001 SUB (memory)
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Bi, Ls | Lo, Tr],                            # 01010 CMI (immediate)
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Pc | Ro | Bi, Bo | Mi, Ro | Bi, Ls | Lo],              # 01011 CMP (memory)
    [0],                                                                                    # 01100
    [0],                                                                                    # 01101
    [0],                                                                                    # 01110
    [0],                                                                                    # 01111
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],                                          # 10000 JMP
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],                                          # 10001 JC (flag dependent)
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],                                          # 10010 JZ (flag dependent)
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],                                          # 10011 JNZ (flag dependent)
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi | Pr, Tr],                                     # 10100 PAGE0
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi | Ps, Tr],                                     # 10101 PAGE1
    [Po | Mi, Pc | Ro | Ci, Xc, Tr],                                                        # 10110 RESET
    [0],                                                                                    # 10111
    [Po | Mi, Pc | Ro | Ci, Ao | Oi, Tr],                                                   # 11000 OUTA
    [Po | Mi, Pc | Ro | Ci, Ao | Oi, Tr],                                                   # 11001 OUTB
    [Po | Mi, Pc | Ro | Ci, Ao | Oi, Tr],                                                   # 11010 OUTC
    [Po | Mi, Pc | Ro | Ci, Ao | Oi, Tr],                                                   # 11011 OUTD
    [Po | Mi, Pc | Ro | Ci, Ao | Oi, Tr],                                                   # 11100 OUTE
    [Po | Mi, Pc | Ro | Ci, Ao | Oi, Tr],                                                   # 11101 OUTF
    [Po | Mi, Pc | Ro | Ci, Io | Ai, Tr],                                                   # 11110 INA
    [Po | Mi, Pc | Ro | Ci, Io | Ai, Tr],                                                   # 11111 INB

]

# Flag dependent instruction matrices [C, Z]

jc_flags = [
    [Po | Mi, Pc | Ro | Ci, Pc, Tr],
    [Po | Mi, Pc | Ro | Ci, Pc, Tr],
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],
]

jz_flags = [
    [Po | Mi, Pc | Ro | Ci, Pc, Tr],
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],
    [Po | Mi, Pc | Ro | Ci, Pc, Tr],
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],
]

jnz_flags = [
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],
    [Po | Mi, Pc | Ro | Ci, Pc, Tr],
    [Po | Mi, Pc | Ro | Ci, Po | Mi, Ro | Pi, Tr],
    [Po | Mi, Pc | Ro | Ci, Pc, Tr],
]


def build(flags, opcode, step):
    matrix[JC] = jc_flags[flags]
    matrix[JZ] = jz_flags[flags]
    matrix[JNZ] = jnz_flags[flags]
    return matrix[opcode][step]
