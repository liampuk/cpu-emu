# SAP-1 Emulator Extended

This is a simulation of the SAP-1 computer from Digital Computer Electronics with a few additional operations. These additions make this computer turing complete, meaning it can compute anything any other computer can (except for the fact it only has 16 bytes of memory). [Ben Eater's](https://www.youtube.com/c/beneater) videos are incredible at explaining how the additional operations work and the reasons behind adding them.

### Specs

- 8-bit address/data bus
- 4-bit opcodes
- 4-bit address width
- 16 bytes of memory

### Instruction Set

| Instruction | Opcode | Description                           |
| ----------- | ------ | ------------------------------------- |
| NOP         | 0000   | no operation                          |
| LDA         | 0001   | load accumulator                      |
| ADD         | 0010   | add to accumulator                    |
| SUB         | 0011   | subtract from accumulator             |
| OUT         | 0100   | output accumulator                    |
| STA         | 0100   | store accumulator in memory           |
| LDI         | 0100   | load immediate value into accumulator |
| JMP         | 0100   | jump                                  |
| JC          | 0100   | jump if carry flag is set             |
| JZ          | 0100   | jump if zero flag is set              |
| JNZ         | 0100   | jump if zero flag is not set          |
| HLT         | 1111   | halt clock                            |

### Assembler

The assembler takes an input `.asm` file and outputs to `bin/` if an output file name is specified. `-v` prints the output bytecode eg:

`python assembler.py -i programs/loop.asm -o a.out -v`

### Simulator

The simulator can take bytecode, binary files or assembly files as an input, eg:

`python simulator.py -b 000100101111000000000010`

or

`python simulator.py -f bin/a.out`

or

`python simulator.py -a programs/loop.asm`
