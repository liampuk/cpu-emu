# Flat-8 emulator

This emulator is a proof of concept for a breadboard computer I plan to build. It is based on the SAP-1 computer described in Digital Computer Electronics, with an expanded instruction set, extra outputs, paging for addressing rom/ram and an 8-bit address width. This emulator is an extension of the [SAP-8](https://github.com/liampuk/cpu-emu/tree/main/sap_8).

The extra I/O will be used to support several expansion boards:
- PS/2 Keyboard controller
- VGA display
- Cartridge loader

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