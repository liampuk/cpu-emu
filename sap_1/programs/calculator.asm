; Test calculator program


lda a   ; load contents of a (4) into accumulator
add b   ; add contents of b (2) to accumulator
sub c   ; subtract contents of c (1) from accumulator
out     ; output accumulator
hlt     ; halt clock

a: db 4
b: db 2
c: db 1