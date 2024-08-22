# SAP-8 Emulator

This CPU design is based on the _SAP-1 extended_ but with an 8 bit address width and slightly expanded instruction set.

## Usage

### Assembler

The assembler takes an input `.asm` file and outputs to `bin/` if an output file name is specified. `-v` prints the output bytecode eg:

`python assembler.py -i programs/loop.asm -o a.out -v`

To inspect the output file, use

`hexdump -e '1/1 "%02X " "\n"' bin/a.out`

### Simulator

The simulator can take bytecode, binary files or assembly files as an input, eg:

`python simulator.py -b 000100101111000000000010`

or

`python simulator.py -f bin/a.out`

or

`python simulator.py -a programs/loop.asm`

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

- ADD/SUB with memory address mode
- 6 outputs, 2 inputs
- Compare (set flags but don't update accumulator)
- Change page bit
- Reset cpu

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
| CMP [15]    | 01011  | compare memory address to accumulator (set flags) |         |
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

These instructions are assembler directives and control how code is assembled. In addition to these codes, labels can be used to reference locations.

```
    LDI 0       ; Load accumulator with 0
  
Func:           ; Func subroutine
    ADD 4       ; Add 4 to accumulator
    OUTA        ; Output accumulator
    JMP Start   ; Jump to Func subroutine
```

 The assembler ignores comments that start with `;`.

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

For read operations the page bit determines if ROM or RAM should be used. Write operations always go to RAM. This allows for easy loading from peripherals to RAM, as the page does not need to be changed when writing while in Page 0 (ROM).

- input to ROM should be `!page AND Ro`: if page is low and Ro high, enable ROM out
- input to RAM should be `page AND Ro`: if page is high and Ro high, enable RAM out

<details>
<summary>Extensions</summary>

## Design

- Perma-Proto permanent breadboard pcbs: https://www.adafruit.com/product/1606
- Spray paint stripboard for rails: https://www.instagram.com/p/Crv-0g0PAhX/
- Black wood back panel
- Dark wood frame
- Clear perspex cover, with switches mounted and labels
- Aluminium bottom panel
  - Keyboard (cutout only relevant keys, usb to ps/2 interface)
  - Manual control switches (run/clock speed etc.)

```
[ DISP ]    [ VGA  ]      Display and VGA controller
[ DISP ]    [ VGA  ]      Display and VGA controller
[ IO   ] || [ IO   ]      4 outputs
[ CLK  ] || [ 7SEG ]      Clock and 7 segment output
[ ROM  ] || [ REGA ]      ROM and A register
[ MAR  ] || [ ALU  ]      MAR and ALU
[ RAM  ] || [ REGB ]      RAM and B register
[ IR   ] || [ CTR  ]      IR and control logic
[ IO   ] || [ IO   ]      1 output, 2 inputs
[ KEYB ]    [ CART ]      Keyboard controller, cartridge loader
--------------------
 xx [ KEYBOARD ] xx       Keyboard and manual control switches
 xx [ KEYBOARD ] xx       Keyboard and manual control switches
```

### Controls

- Reset
- Manual control (disables control, enables manual programming switches)
- Clock speed
- Single step
- Run

- CPU manual programming
  - Bus
  - MAR in
  - RAM in
  - PC in
  - Increment PC

## Keyboard

### Requires

- 1 input register
- I/O is combined with enable (9-pin I/O)
- PS/2 keyboard controller board

### Keyboard Controller

- Shift in data from PS/2
- Disable shift register when count is 11
  - this means lifts are ignored, either cpu doesn't read before key is lifted and the lift is not registered, or cpu reads before lift, but then the lift code is shifted in and mapped to nothing and cleared for next keypress. This does mean keypresses won't be accepted until the cpu reads and clears the lift in this case.
- On negative edge of input enable - reset count and clear shift register.
  - if no key pressed, the next read will be a 0 (or mapped value) and the cpu will continue to loop
  - if a new key is pressed, it can be shifted in and read.

## Display

### Requires

- 3 output registers
  - X, Y and data
- I/O is combined with enable (9-pin I/O)
- VGA controller board

### VGA Controller

- X, Y address VRAM, data is character
- rising edge of enable on X = disable write to VRAM
- falling edge of enable on Data = enable write to VRAM

- VRAM write enable AND with blanking interval.

## Cartridge interface

### Requires

- 1 output, 1 input
- GBA cartridge slot

### GBA cartridge loader

- GBA games are stored after x0100
- So can store code on x0000 - x00FF and leave game intact (lol)
- Controller should be simple, output address and read data.

</details>
