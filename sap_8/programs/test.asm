; Test program

    ldi 0       ; load 0 into accumulator

start:
    add a       ; add contents of a (16) into accumulator
    outa        ; output accumulator
    jc stop     ; jump to address 5 if the carry flag is set
    jmp start   ; jump to address 1

stop:
    hlt         ; halt clock

a:  db 16       ; store 16 in memory

    org 12
    db 1

    org 255
    db 255