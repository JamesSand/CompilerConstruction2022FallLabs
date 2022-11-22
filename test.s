    .text
    .global main

main:
    # start of prologue
    addi sp, sp, -96
    sw ra, 44(sp)
    sw fp, 48(sp)
    addi fp, sp, 96
    # end of prologue

    # start of body
    li t0, 0 
    mv t1, t0 # t1 ret
    li t0, 0
    mv t2, t0 # i
    sw t1, 52(sp) # ret 52
    sw t2, 56(sp) # i 56
_L1:
    li t0, 100 
    lw t1, 56(sp) # t1 i
    slt t2, t1, t0 
    sw t1, 56(sp) # i 56
    beq x0, t2, _L3
    li t0, 2
    lw t1, 56(sp) # t1 i
    rem t2, t1, t0 
    mv t0, t2 # result t0 arg1
    li t2, 3
    rem t3, t1, t2
    mv t2, t3 # result t2 arg2
    li t3, 5
    rem t4, t1, t3
    mv t3, t4 # t3 arg3
    li t4, 7
    rem t5, t1, t4
    mv t4, t5 # arg4
    li t5, 11
    rem t6, t1, t5
    mv t5, t6
    li t6, 13
    rem a0, t1, t6
    mv t6, a0
    li a0, 17
    rem a1, t1, a0
    mv a0, a1
    li a1, 19
    rem a2, t1, a1
    mv a1, a2
    
    sw t0, 60(sp)
    sw t1, 56(sp)
    sw t2, 64(sp)
    sw t3, 68(sp)
    sw t4, 72(sp)
    sw t5, 76(sp)
    sw t6, 80(sp)
    sw a0, 84(sp)
    sw a1, 88(sp)
    sw a2, 92(sp)

    lw a0, 60(sp)
    lw a1, 64(sp)
    lw a2, 68(sp)
    lw a3, 72(sp)
    lw a4, 76(sp)
    lw a5, 80(sp)
    lw a6, 84(sp)
    lw a7, 88(sp)
    call read_arg_reg_8
    lw t0, 60(sp)
    lw t1, 56(sp)
    lw t2, 64(sp)
    lw t3, 68(sp)
    lw t4, 72(sp)
    lw t5, 76(sp)
    lw t6, 80(sp)
    lw a0, 84(sp)
    lw a1, 88(sp)
    lw a2, 92(sp)
    mv t0, a0
    lw t2, 52(sp)
    add t3, t2, t0
    mv t2, t3
    sw t2, 52(sp)
    sw t1, 56(sp)
_L2:
    li t0, 1
    lw t1, 56(sp)
    add t2, t1, t0
    mv t1, t2
    sw t1, 56(sp)
    j _L1
_L3:
    lw t0, 52(sp)
    mv a0, t0
    j main_exit
    # end of body

main_exit:
    # start of epilogue
    lw ra, 44(sp)
    lw fp, 48(sp)
    addi sp, sp, 96
    # end of epilogue

    ret