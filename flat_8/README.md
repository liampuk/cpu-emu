# Flat-8 emulator

This emulator is a proof of concept for a breadboard cpu I plan to build. The plan:

- 8-bit address width
- page bit for addressing rom/ram
- keyboard controller
  - this requires interrupts and 1 input register.
  - characters encoded into 6 bits (64 characters), with shift bit for capitals and highlight bit for inverted colours (1 byte each)
- text [vga](https://www.youtube.com/watch?v=LCPOXZ7zaD0) output
  - this requires 3 output registers (vertical and horizontal vram address, data)
  - hold characters in vram, write to vram during blanking intervals
  - cpu clock is slow enough that timing isn't an issue
  - [sr latch for toggling write mode](https://youtu.be/t3Bym8pGhn4?t=83)
    - when x register updated, disable write
    - when data register updated, enable write
    - this prevents writing data to the wrong location during an address update from the cpu (requires updating registers in the order x > y > data)
  - see [here](http://tinyvga.com/vga-timing/800x600@60Hz) for vga timings
  - plan
    - 400x240 resolution
    - 50x30 characters
    - 16 bit counter addresses vram
    - vram byte + low 3 bits of high 8 bits of counter address (low 3 bits correspond to each row of character byte) character rom (AT28C16-20PC)
      - low 8 bits of 16 bit counter map exactly to the horizontal count
      - next 3 bits of higher 8 bits of 16 bit counter map to character lines
- rom bootloader
  - requires 1 input register, 1 output register
  - cartridge slot for rom (gb cartridge?)
  - paging flag determines reads, write ignores paging flag. This means the bootloader can execute and store input values to ram, then when finished can set the paging bit to 1 and reset the pc
    - This must be done in one instruction, ie. `PAGE 1 00` would set the page bit to read from RAM and jump to address 0
  - see [here](https://cronop-io.github.io/posts/retrocomputing,%20binary%20analysis,%20hardware/2020-11-25-GameBoyPart1/) for interfacing with a gb cartridge
- one output should display on 7-segment (probably vga data)
- inputs/outputs should be 9 pin connectors, with 1 pin for interrupts and output enables (output enable can be used as an interrupt from the cpu to a peripheral device)
- db9 cable for outputs, 9 pin din for inputs

The name is a reference to the [DEC *Straight-8* (PDP-8)](https://collection.sciencemuseumgroup.org.uk/objects/co8061113/dec-pdp-8-minicomputer-1965-minicomputers-computers), but of course this computer is flat, because it will be built on breadboards. (I know this is daft)

### TODO
- only 1 temporary register needed for the alu?
- address input/output ports? (to save control lines)
- add reset t-state control line
- page bit (flags?)
  - set using temporary register? 
- EEPROM
  - 8 bit word = 256 control lines, decode 6 lsb = 64
  - addressed by opcode flags (PSCZ), and I flag AND with interrupt line = 8 + 4 + 1 = 13
  - Atmel 28C64 - 64Kb, 8k words (13 bit address)
- Does IO use the accumulator?
- Should memory operations only use accumulator to simplify?

### Software

- ROM
  - Check if xFF at address zero on cartridge
  - If yes, load cartridge program into ram
  - If no, memory editor (using keyboard)
- Text editor
  - input from keyboard, render characters on screen. Should handle new lines, backspaces

## Components

### CPU

#### Requirements

- 8 bit opcodes, 8 bit addresses
- Registers
  - Accumulator
  - General purpose registers (B, C)
  - Stack pointer
  - Flags
  - PC, IR, MAR
  - 5 output, 2 input registers
- Interrupts

#### Instruction Set

Very loosely based on x86, following [this example](https://nbest.co.uk/Softwareforeducation/sms32v50/sms32v50_manual/245-IsetSummary.htm).

Note: revisit this after writing programs, to remove if not needed. There will also be more instructions available to the assembler (`CMP`), but these can be implemented with macros.

**Move instructions**
- `MOV A, 15` : load accumulator with 15
- `LDI A, [15]` : load RAM at address 15 into A
- `LDR A, [B]` : load RAM at address B into A
- `STI [15], A` : load A into RAM at address 15
- `STR [B], A` : load A into RAM at address in B

**Arithmatic instructions (sets flags, register and immediate modes)**
- `ADD A, B` / `ADD A, 15`
- `SUB A, B` / `SUB A, 15`
- `AND A, B` / `AND A, 15`
- `OR A, B` / `OR A, 15`
- `XOR A, B` / `XOR A, 15`

**Branch instructions**
- `JMP`
- `JZ` / `JNZ`
- `JS` / `JNS`
- `JC` / `JNC`
- `MPAGE [15]`
- `SPAGE [15]`

**Stack instructions**
- `CALL 30` push PC to the stack and jump to 30
- `PUSH A` / `POP A` :  push/pop A to/from the stack
- `PUSHF` / `POPF` : push/pop from/to the flags register

**IO instructions**
- `IN 2` : input from io port 2
- `OUT 4` : output to io port 4

**Misc instructions**
- `HLT` : halt
- `NOP` : no operation
- `STI` : enable interrupts
- `CLI` : disable interrupts

**Assembler instructions**
- `ORG 40` : generate code from address 40
- `DB 15` : define byte


| Instruction | Opcodes | Description                                      |
|-------------|---------|--------------------------------------------------|
| NOP         | 00      | no operation                                     |
| MOV R, I    | 01 - 03 | load immediate value to register                 |
| LDI R, [I]  | 04 - 06 | load address at immediate value to register      |
| LDR R, [R]  | 07 - 0C | load address at register to register             |
| STI [I], R  | 0D - 0F | store register at immediate address              |
| STR [R], R  | 10 - 15 | store register at register address               |
| ADD R, R    | 16 - 1B | add register to register                         |
| ADD R, I    | 1C - 1E | add immediate value to register                  |
| SUB R, R    | 1F - 24 | subtract register from register                  |
| SUB R, I    | 25 - 27 | subtract immediate value from register           |
| AND R, R    | 28 - 2D | and register with register                       |
| AND R, I    | 2E - 30 | and immediate value with register                |
| 0R R, R     | 31 - 36 | or register with register                        |
| 0R R, I     | 37 - 39 | or immediate value with register                 |
| X0R R, R    | 3A - 3F | xor register with register                       |
| X0R R, I    | 40 - 42 | xor immediate value with register                |
| JMP I       | 41      | jump immediate                                   |
| JZ I        | 42      | jump if zero                                     |
| JNZ I       | 43      | jump if not zero                                 |
| JS I        | 44      | jump if negative                                 |
| JNS I       | 45      | jump if not negative                             |
| JC I        | 46      | jump on carry                                    |
| JNC I       | 47      | jump on no carry                                 |
| CALL I      | 48      | call subroutine (push pc to stack)               |
| RET         | 49      | return from subroutine (pop pc from stack)       |
| IRET        | 50      | return from interrupt (re-enable interrupt flag) |
| PUSH R      | 51 - 53 | push registers to stack                          |
| POP R       | 54 - 56 | pop stack to registers                           |
| PUSHF       | 57      | push flags register to stack                     |
| POPF        | 58      | pop flags from stack to register                 |
| IN I        | 59 - 60 | input from io port I                             |
| OUT I       | 61 - 65 | output to io port I                              |
| STI         | 66      | enable interrupts                                |
| CLI         | 67      | disable interrupts                               |
| ...         | ...     | ...                                              |
| HLT         | 255     | halt                                             |

#### Microcode considerations

- Most instructions are explicit in what they need the cpu to do (`JMP` always means jump to an immediate value). Some are less so, like `MOV`, this instruction moves an immediate value into any of the general purpose registers, and so needs to be compiled to 3 different opcodes depending on the destination.
- For instructions dependent on flags, like `JNZ`, the microcode needs to be indexed with the opcode and the flags register
- For Interrupts, the microcode needs to be indexed with the flags register (interrupt enable flag) and the interrupt line

### VGA Circuit

The VGA circuit outputs a standard 640 x 480 @ 60Hz timing signal. This will be implemented using a 16MHz oscillator, so is slightly out of spec but should be fine. Output will be in text mode only, with a resolution of 50 x 30 characters (400 x 240 pixels). This design is heavily based off [this series](https://www.youtube.com/watch?v=LCPOXZ7zaD0) by Slu4.

To generate the timings and index VRAM a 16 bit counter is used. As one line takes the equivalent of 64 counts, the lower 6 bits (`HA`) are used to generate the horizontal timing and as the lower order VRAM address byte corresponding to values the cpu writes to register X.

The next bit (`SB`) is skipped to halve the vertical resolution to 240 pixels.

The next 3 bits (`CRI`) are used to index the row of the character currently pointed to by VRAM (characters are stored as 8 rows of bytes).

The next 5 bits (`VA`) as used as the higher order VRAM address byte corresponding to values the cpu writes to register Y. Only 5 bits are required as only 30 characters can be rendered vertically (30 * 8 = 240 pixels).

The last bit (`RB`) is used to allow the counter to reach 520 where it is reset.

#### Counter value timings

- Horizontal
  - 0 - 49  VRAM address
  - 50 - 51 Front porch (high pulse)
  - 52 - 59 Sync pulse (low pulse)
  - 60 - 63 Back porch (high pulse)
- Vertical
  - 0 - 479 VRAM address
  - 480 - 487 Front porch (high pulse)
  - 488 - 489 Sync pulse (low pulse)
  - 490 - 519 Back porch (high pulse)

The way these counts are converted into timing signals is very well explained in [this video](https://www.youtube.com/watch?v=l7rce6IQDWs) from Ben Eater. AND gates are used (fed with inverted/non-inverted lines from the count to equal exact counts) to set 2 SR latches for when pixel data should be shown, and the sync pulse.

![image](https://user-images.githubusercontent.com/17195367/219518868-c735a553-0020-4292-b746-d2a64722a8ce.png)

#### Timing

- Spec Pixel Frequency: 25.175Mhz
- Actual Clock: 16Mhz

#### Horizontal

| Section     | Time (µs) | Bytes | Pixels | Actual Time (µs) |
|-------------|-----------|-------|--------|------------------|
| Data        | 25.422    | 50    | 400    | 25               |
| Front Porch | 0.636     | 2     | 16     | 1                |
| Sync Pulse  | 3.813     | 8     | 64     | 4                |
| Back Porch  | 1.907     | 4     | 32     | 2                |
| Whole Line  | 31.778    | 64    | 512    | 32               |

#### Vertical

| Section     | Time (ms) | Lines    |
|-------------|-----------|----------|
| Data        | 15.253    | 480      |
| Front Porch | 0.318     | 8 (10?)  |
| Sync Pulse  | 0.064     | 2        |
| Back Porch  | 1.049     | 30 (33?) |
| Whole Page  | 16.683    | 520      |

---

Current progress on emulating a display:
![image](https://user-images.githubusercontent.com/17195367/219976847-c291c90d-acc3-408a-a228-5989a43d04c9.png)
