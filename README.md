# CPU Emulation

This is a collection of cpu emulators, starting with the very simple SAP-1 computer described in Digital Computer Electronics. The aim is to authentically replicate how a cpu would work if built using TTL logic (and hopefully eventually actually build one).

## SAP-1

This is the simplest computer architecture described in Digital Computer Electronics. The cpu only has 16 bytes and only 4 instructions. The only modifications I have made is to add NOP (no operation) and HLT (halt clock) to the instruction set.

![image](https://user-images.githubusercontent.com/17195367/218260669-404ff239-e886-45c5-839d-9562fb4063b1.png)

> [SAP-1](https://github.com/liampuk/cpu-emu/tree/main/sap_1)

## SAP-1 extended

This cpu design is very similar to the SAP-1, with a few extra control lines and opcodes. The addition of conditional jump instructions (JC - jump on carry, JZ - jump on zero, JNZ - jump on not zero) make this cpu turing complete, meaning it can theoretically do anything any other cpu can. This is limited in practice by the fact it can only address 16 bytes of memory.

**Extra instructions**

| Instruction | Opcode | Description                           |
|-------------|--------|---------------------------------------|
| STA         | 0100   | store accumulator in memory           |
| LDI         | 0100   | load immediate value into accumulator |
| JMP         | 0100   | jump                                  |
| JC          | 0100   | jump if carry flag is set             |
| JZ          | 0100   | jump if zero flag is set              |
| JNZ         | 0100   | jump if zero flag is not set          |

> [SAP-1 extended](https://github.com/liampuk/cpu-emu/tree/main/sap_1_extended)
