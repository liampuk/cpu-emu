# SAP-8 Emulator

This CPU design is based on the _SAP-1 extended_ but with an 8 bit address width and slightly expanded instruction set.

## Usage

### Assembler

The assembler takes an input `.asm` file and outputs to `bin/` if an output file name is specified. `-v` prints the output bytecode eg:

`python assembler.py -i programs/loop.asm -o a.out -v`

To inspect the output file, use

`hexdump -e '1/1 "%02X " "\n"' bin/a.out`

### Simulator

The simulator has a hardcoded rom (rom.py). Custom rom and ram can be provided with `-r --rom` and `-m --ram`

`python simulator.py -r bin/a.out`

## Overview

- 8-bit data/address width
  - 256 bytes of RAM
- Accumulator
- Non-addressable B register
- ALU with ADD and SUB
- Flags
  - Z: zero
  - C: carry
- PC, IR, MAR
- 6 Outputs, 2 inputs
- Page bit for ROM/RAM address

## Instruction Set

Based on the sap-1 extended instruction set with a 5 bit opcode allowing for up to 32 instructions. Additional instructions are:

- `ADD/SUB`: add/sub with memory address mode
- `OUTA / OUTB ...`: 6 outputs, 2 inputs
- `CMP`: Compare (set flags but don't update accumulator)
- `PAGE0 / PAGE1`: Change page bit
- `RESET`: Reset cpu

Instructions that use immediate values or a memory address use 2 bytes.

| Instruction | Opcode | Description                                       | 2 bytes |
|-------------|--------|---------------------------------------------------|---------|
| NOP         | 00000  | no operation                                      |         |
| HLT         | 00001  | halt                                              |         |
| LDI 15      | 00010  | load immediate value into accumulator             | x       |
| LDA [15]    | 00011  | load accumulator from memory                      | x       |
| STA 15      | 00100  | store accumulator in memory                       | x       |
| STM [15]    | 00101  | Store accumulator to memory address               | x       |
| ADI 15      | 00110  | add immediate to accumulator                      | x       |
| ADD [15]    | 00111  | add memory address to accumulator                 | x       |
| SUI 15      | 01000  | subtract immediate from accumulator               | x       |
| SUB [15]    | 01001  | subtract memory address from accumulator          | x       |
| CMI 15      | 01010  | compare immediate to accumulator (set flags)      | x       |
| CMP [15]    | 01011  | compare memory address to accumulator (set flags) | x       |
|             | 01100  |                                                   |         |
|             | 01101  |                                                   |         |
|             | 01110  |                                                   |         |
|             | 01111  |                                                   |         |
| JMP 15      | 10000  | jump                                              | x       |
| JC 15       | 10001  | jump if carry flag is set                         | x       |
| JZ 15       | 10010  | jump if zero flag is set                          | x       |
| JNZ 15      | 10011  | jump if zero flag is not set                      | x       |
| PAGE0 15    | 10100  | change page and jump                              | x       |
| PAGE1 15    | 10101  | change page and jump                              | x       |
| RESET       | 10110  | reset cpu                                         |         |
|             | 10111  |                                                   |         |
| OUTA        | 11000  | output accumulator to output A                    |         |
| OUTB        | 11001  | output accumulator to output B                    |         |
| OUTC        | 11010  | output accumulator to output C                    |         |
| OUTD        | 11011  | output accumulator to output D                    |         |
| OUTE        | 11100  | output accumulator to output E                    |         |
| OUTF        | 11101  | output accumulator to output F                    |         |
| INA         | 11110  | input A to accumulator                            |         |
| INB         | 11111  | input B to accumulator                            |         |

### Assembler Instructions

- `ORG` and `DB` instructions are assembler directives and control how code is assembled
- The assembler ignores comments that start with `;`
- Labels can be used to reference locations
- Relative addresses to labels can be used with `+`

```
; Example program

LOADER:                 ; start of loader subroutine
    lda PROGRAM +0      ; load accumulator with program subroutine with relative memory address
    stm 0               ; store in RAM
    lda PROGRAM +1
    stm 1

PROGRAM:                ; subroutine
    db ldi
    db 255
    db hlt
    
    org 30              ; unused byte at memory location 30
    db 255
```

| Instruction | Description                                     |
|-------------|-------------------------------------------------|
| ORG 15      | Assemble following code to this memory location |
| DB 15       | define byte in memory                           |

## Control Word

Four extra control lines needed over SAP-1 extended, giving a total of 21 instructions:

- enable input to bus
- set page bit to 1
- reset page bit to 0
- reset t-state counter

Opcodes are combined with flags and page bit to index the control matrix with 8 bits:

- 5-bit opcode
- 2 bit flags
- 1 bit page

| Signal | Description                |
|--------|----------------------------|
| Ch     | halt clock                 |
| Pc     | increment program counter  |
| Po     | program counter out        |
| Pi     | program counter in         |
| Mi     | memory address register in |
| Ro     | ram out                    |
| Ri     | ram in                     |
| So     | rom out                    |
| Ci     | instruction register in    |
| Co     | instruction register out   |
| Ai     | accumulator in             |
| Ao     | accumulator out            |
| Ls     | alu subtract mode          |
| Lo     | alu out                    |
| Bi     | b register in              |
| Bo     | b register out             |
| Oi     | output register in         |
| Io     | input out                  |
| Ps     | set page                   |
| Pr     | reset page                 |
| Tr     | reset t-state counter      |
| Xc     | reset cpu                  |

### IO operations

For IO operations, the opcode is combined with the control signals to control the cpu:

- IO opcodes (11xxx) map to the control signals `Lo` for output (11000 to 11101) and `Ei` for input (11110 to 11111). The low 3 bits of the opcode is used to control which input/output line is enabled

#### IO operations

| Instruction | Opcode | Control signal for IO | IO opcode address | Active IO |
|-------------|--------|-----------------------|-------------------|-----------|
| OUTA        | 11000  | Lo                    | 11[000]           | Output A  |
| OUTB        | 11001  | Lo                    | 11[001]           | Output B  |
| OUTC        | 11010  | Lo                    | 11[010]           | Output C  |
| OUTD        | 11011  | Lo                    | 11[011]           | Output D  |
| OUTE        | 11100  | Lo                    | 11[100]           | Output E  |
| OUTF        | 11101  | Lo                    | 11[101]           | Output F  |
| INA         | 11110  | Ei                    | 11[110]           | Input A   |
| INB         | 11111  | Ei                    | 11[111]           | Input B   |

### Paging

For read operations the page bit determines if ROM or RAM should be used. Write operations always go to RAM. This allows for easy loading from peripherals to RAM, as the page does not need to be changed when executing from ROM.
- Access to ROM/RAM is controlled by the `So` (Storage out - ROM) and `Ro` (Ram out) control lines.
