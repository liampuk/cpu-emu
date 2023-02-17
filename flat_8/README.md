# Flat-8 emulator

This emulator is a proof of concept for a breadboard cpu I plan to build. The plan:

- 8-bit address width
- page bit for addressing rom/ram
- keyboard controller
  - this requires interrupts and 1 input register.
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
    - vram byte + low 3 bits of high 8 bits of counter address (low 3 bits correspond to each row of character byte) character rom
      - low 8 bits of 16 bit counter map exactly to the horizontal count
      - next 3 bits of higher 8 bits of 16 bit counter map to character lines
- rom bootloader
  - requires 1 input register, 1 output register
  - cartridge slot for rom (gb cartridge?)
  - paging flag determines reads, write ignores paging flag. This means the bootloader can execute and store input values to ram, then when finished can set the paging bit to 1 and reset the pc
    - This must be done in one instruction, ie. `PAGE 1 00` would set the page bit to read from RAM and jump to address 0
  - see [here](https://cronop-io.github.io/posts/retrocomputing,%20binary%20analysis,%20hardware/2020-11-25-GameBoyPart1/) for interfacing with a gb cartridge
- one output should display on 7-segment (probably vga data)

The name is a reference to the [DEC *Straight-8* (PDP-8)](https://collection.sciencemuseumgroup.org.uk/objects/co8061113/dec-pdp-8-minicomputer-1965-minicomputers-computers), but of course this computer is flat, because it will be built on breadboards. (I know this is daft)

## Components

### VGA Circuit

![image](https://user-images.githubusercontent.com/17195367/219518868-c735a553-0020-4292-b746-d2a64722a8ce.png)

The VGA circuit outputs a standard 640 x 480 @ 60HZ timing signal. This will be implemented using a 16MHz oscillator, so is slightly out of spec but should be fine. Output will be in text mode only, with a resolution of 50 x 30 characters (400 x 240 pixels).

To generate the timings and index VRAM a 16 bit counter is used. As one line takes the equivalent of 64 counts, the lower 6 bits (`HA`) are used to generate the horizontal timing and as the lower order VRAM address byte corresponding to values the cpu writes to register X.

The next bit (`SB`) is skipped to halve the vertical resolution to 240 pixels.

The next 3 bits (`CRI`) are used to index the row of the character currently pointed to by VRAM (characters are stored as 8 rows of bytes).

The next 5 bits (`VA`) as used as the higher order VRAM address byte. Only 5 bits are required as only 30 characters can be rendered vertically (30 * 8 = 240 pixels).

The last bit (`RB`) is used to allow the counter to reach 520 where it is reset.

#### Counter value timings

- Horizontal
  - 0 - 50  VRAM address
  - 51 - 52 Front porch (high pulse)
  - 53 - 60 Sync pulse (low pulse)
  - 61 - 64 Back porch (high pulse)
- Vertical
  - 0 - 480 VRAM address
  - 481 - 488 Front porch (high pulse)
  - 489 - 490 Sync pulse (low pulse)
  - 490 - 520 Back porch (high pulse)

#### Horizontal Timing

| Section     | Time (µs) | Bytes |
|-------------|-----------|-------|
| Data        | 25.422    | 50    |
| Front Porch | 0.636     | 2     |
| Sync Pulse  | 3.813     | 8     |
| Back Porch  | 1.907     | 4     |
| Whole Line  | 31.778    | 64    |

#### Vertical Timing

| Section     | Time (ms) | Lines |
|-------------|-----------|-------|
| Data        | 15.253    | 480   |
| Front Porch | 0.318     | 8     |
| Sync Pulse  | 0.064     | 2     |
| Back Porch  | 1.049     | 30    |
| Whole Page  | 16.683    | 520   |

