# CPU Emulation

This is a simulation of the SAP-1 computer from Digital Computer Electronics.

### Architecture

![image](https://user-images.githubusercontent.com/17195367/216844700-a00c0eab-8296-4573-83d3-dc027b6c04e4.png)

### Specs

- 8 bit address/data bus
- 4 bit opcodes
- 4 bit address width
- 16 bytes of memory

Example output during an LDA instruction:

```
bus 00000000 | clk 0 | t_state 0 | pc 0 | mar 0 | ir 00000000 | alu 0 | reg_a 0 | reg_b  0 | out 0 | control word 000000000000 | control active []
bus 00000000 | clk 1 | t_state 0 | pc 0 | mar 0 | ir 00000000 | alu 0 | reg_a 0 | reg_b  0 | out 0 | control word 011000000000 | control active ['Lm', 'Ep']
bus 00000000 | clk 1 | t_state 1 | pc 1 | mar 0 | ir 00000000 | alu 0 | reg_a 0 | reg_b  0 | out 0 | control word 100000000000 | control active ['Cp']
bus 00010101 | clk 1 | t_state 2 | pc 1 | mar 0 | ir 00010101 | alu 0 | reg_a 0 | reg_b  0 | out 0 | control word 000110000000 | control active ['Li', 'CE']
bus 00000101 | clk 1 | t_state 3 | pc 1 | mar 5 | ir 00010101 | alu 0 | reg_a 0 | reg_b  0 | out 0 | control word 001001000000 | control active ['Ei', 'Lm']
bus 00000100 | clk 1 | t_state 4 | pc 1 | mar 5 | ir 00010101 | alu 4 | reg_a 4 | reg_b  0 | out 0 | control word 000100100000 | control active ['La', 'CE']
bus 00000100 | clk 1 | t_state 5 | pc 1 | mar 5 | ir 00010101 | alu 4 | reg_a 4 | reg_b  0 | out 0 | control word 000000000000 | control active []
```
