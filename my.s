    .bss
    .global a
a:
    .space 4
    .text
    .global main
    
main:
    # start of prologue
    addi sp, sp, -32
    sw a0, 0(sp)
    sw a1, 4(sp)
    sw a2, 8(sp)
    sw a3, 12(sp)
    sw a4, 16(sp)
    sw a5, 20(sp)
    sw a6, 24(sp)
    sw a7, 28(sp)
    addi sp, sp, -52
    sw ra, 44(sp)
    sw fp, 48(sp)
    addi fp, sp, 52
    # end of prologue
    
    # start of body
    la t0, a
    lw t1, 0(t0)
    li t0, 0
    li t2, 0
    li t3, 1
    mul t0, t0, t3
    add t2, t2, t0
    li t0, 4
    mul t2, t2, t0
    add t1, t1, t2
    lw t0, 0(t1)
    li t0, 24
    mv t2, t0
    sw t2, 0(t1)
    la t0, a
    lw t1, 0(t0)
    li t0, 0
    li t2, 0
    li t3, 1
    mul t0, t0, t3
    add t2, t2, t0
    li t0, 4
    mul t2, t2, t0
    add t1, t1, t2
    lw t0, 0(t1)
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    lw ra, 44(sp)
    lw fp, 48(sp)
    addi sp, sp, 52
    addi sp, sp, 32
    # end of epilogue
    
    ret
    

