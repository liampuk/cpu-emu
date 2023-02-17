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

## Components

### VGA Circuit

![image](https://user-images.githubusercontent.com/17195367/219518868-c735a553-0020-4292-b746-d2a64722a8ce.png)

The name is a reference to the [DEC *Straight-8* (PDP-8)](https://collection.sciencemuseumgroup.org.uk/objects/co8061113/dec-pdp-8-minicomputer-1965-minicomputers-computers), but of course this computer is flat, because it will be built on breadboards. (I know this is daft)
