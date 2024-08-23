; Page test program

LOADER:                 ; start of loader subroutine
    lda PROGRAM +0      ; load accumulator with program subroutine with relative memory address
    stm 0               ; store in RAM
    lda PROGRAM +1
    stm 1
    lda PROGRAM +2
    stm 2
    lda PROGRAM +3
    stm 3
    page1 0             ; swap page to ram and jump to address 0

PROGRAM:                ; subroutine to output FF and halt
    db ldi
    db 255
    db outa
    db hlt