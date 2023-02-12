# Flat-8 emulator

This is an emulator of a breadboard cpu I plan to build. The plan:

- 8-bit address width
- page bit for addressing rom/ram
- keyboard controller
  - this requires interrupts and 1 input register.
- text vga output (this requires 3 outputs)
  - this requires 3 output registers (vertical and horizontal vram address, data)
  - hold characters in vram, write to vram during blanking intervals
  - cpu clock is slow enough that timing isn't an issue
  - see [here](http://tinyvga.com/vga-timing/800x600@60Hz) for vga timings
- rom bootloader
  - requires 1 input register, 1 output register
  - cartridge slot for rom (gb cartridge?)
  - see [here](https://cronop-io.github.io/posts/retrocomputing,%20binary%20analysis,%20hardware/2020-11-25-GameBoyPart1/) for interfacing with a gb cartridge

The name is a reference to the *Straight-8* (PDP-8), but of course this computer is flat, because it will be built on breadboards. (I know this is daft)