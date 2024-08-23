; Sum test program

    ldi 0       ; load 0 into accumulator

start:
    adi 15      ; add immediate 15 to accumulator
    outa        ; output accumulator
    jc stop     ; jump to stop subroutine if the carry flag is set
    jmp start   ; jump to start subroutine

stop:
    hlt         ; halt clock
