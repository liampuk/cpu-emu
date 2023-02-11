; Conditional loop program

    ldi 0       ; load 0 into accumulator

start:
    add a       ; add contents of a (2) into accumulator
    out         ; output accumulator
    jc stop     ; jump to address 4 if the carry flag is set
    jmp start   ; jump to address 1

stop:
    hlt         ; halt clock

a:  db 2        ; store 2 in memory