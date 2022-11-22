    .text
    .global main
    
main:
    # start of prologue
    addi sp, sp, -120
    sw s1, 0(sp)
    sw s2, 4(sp)
    sw s3, 8(sp)
    sw s4, 12(sp)
    sw ra, 44(sp)
    sw fp, 48(sp)
    addi fp, sp, 120
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    sw t1, 52(sp)
_L1:
    li t0, 100
    lw t1, 52(sp)
    slt t2, t1, t0
    sw t1, 52(sp)
    beq x0, t2, _L3
    li t0, 0
    mv t1, t0
    li t0, 0
    mv t2, t0
    li t0, 0
    mv t3, t0
    li t0, 0
    mv t4, t0
    li t0, 0
    mv t5, t0
    li t0, 0
    mv t6, t0
    li t0, 0
    mv a1, t0
    li t0, 0
    mv a2, t0
    li t0, 0
    mv a3, t0
    li t0, 0
    mv a4, t0
    li t0, 0
    mv a5, t0
    li t0, 0
    mv a6, t0
    li t0, 0
    mv a7, t0
    li t0, 0
    mv s1, t0
    li t0, 0
    mv s2, t0
    li t0, 0
    mv s3, t0
    sw t0, 56(sp)
    sw t1, 60(sp)
    sw t2, 64(sp)
    sw t3, 68(sp)
    sw t4, 72(sp)
    sw t5, 76(sp)
    sw t6, 80(sp)
    sw a1, 84(sp)
    sw a2, 88(sp)
    sw a3, 92(sp)
    sw a4, 96(sp)
    sw a5, 100(sp)
    sw a6, 104(sp)
    sw a7, 108(sp)
    lw a0, 60(sp)
    lw a1, 64(sp)
    call hash
    lw t0, 56(sp)
    lw t1, 60(sp)
    lw t2, 64(sp)
    lw t3, 68(sp)
    lw t4, 72(sp)
    lw t5, 76(sp)
    lw t6, 80(sp)
    lw a1, 84(sp)
    lw a2, 88(sp)
    lw a3, 92(sp)
    lw a4, 96(sp)
    lw a5, 100(sp)
    lw a6, 104(sp)
    lw a7, 108(sp)
    mv t0, a0
    sw t0, 112(sp)
    sw t1, 60(sp)
    sw t2, 64(sp)
    sw t3, 68(sp)
    sw t4, 72(sp)
    sw t5, 76(sp)
    sw t6, 80(sp)
    sw a1, 84(sp)
    sw a2, 88(sp)
    sw a3, 92(sp)
    sw a4, 96(sp)
    sw a5, 100(sp)
    sw a6, 104(sp)
    sw a7, 108(sp)
    lw a0, 68(sp)
    lw a1, 72(sp)
    call hash
    lw t0, 112(sp)
    lw t1, 60(sp)
    lw t2, 64(sp)
    lw t3, 68(sp)
    lw t4, 72(sp)
    lw t5, 76(sp)
    lw t6, 80(sp)
    lw a1, 84(sp)
    lw a2, 88(sp)
    lw a3, 92(sp)
    lw a4, 96(sp)
    lw a5, 100(sp)
    lw a6, 104(sp)
    lw a7, 108(sp)
    mv s4, a0
    sw t0, 112(sp)
    sw t1, 60(sp)
    sw t2, 64(sp)
    sw t3, 68(sp)
    sw t4, 72(sp)
    sw t5, 76(sp)
    sw t6, 80(sp)
    sw a1, 84(sp)
    sw a2, 88(sp)
    sw a3, 92(sp)
    sw a4, 96(sp)
    sw a5, 100(sp)
    sw a6, 104(sp)
    sw a7, 108(sp)
    lw a0, 112(sp)
    mv a1, s4
    call hash
    lw t0, 112(sp)
    lw t1, 60(sp)
    lw t2, 64(sp)
    lw t3, 68(sp)
    lw t4, 72(sp)
    lw t5, 76(sp)
    lw t6, 80(sp)
    lw a1, 84(sp)
    lw a2, 88(sp)
    lw a3, 92(sp)
    lw a4, 96(sp)
    lw a5, 100(sp)
    lw a6, 104(sp)
    lw a7, 108(sp)
    mv t0, a0
    mv s4, t0
    sw t0, 116(sp)
    sw t1, 60(sp)
    sw t2, 64(sp)
    sw t3, 68(sp)
    sw t4, 72(sp)
    sw t5, 76(sp)
    sw t6, 80(sp)
    sw a1, 84(sp)
    sw a2, 88(sp)
    sw a3, 92(sp)
    sw a4, 96(sp)
    sw a5, 100(sp)
    sw a6, 104(sp)
    sw a7, 108(sp)
    addi sp, sp, -32
    sw a3, 0(sp)
    sw a4, 4(sp)
    sw a5, 8(sp)
    sw a6, 12(sp)
    sw a7, 16(sp)
    sw s1, 20(sp)
    sw s2, 24(sp)
    sw s3, 28(sp)
    lw a0, 92(sp)
    lw a1, 96(sp)
    lw a2, 100(sp)
    lw a3, 104(sp)
    lw a4, 108(sp)
    lw a5, 112(sp)
    lw a6, 116(sp)
    lw a7, 120(sp)
    call read_arg_reg_16
    addi sp, sp, 32
    lw t0, 116(sp)
    lw t1, 60(sp)
    lw t2, 64(sp)
    lw t3, 68(sp)
    lw t4, 72(sp)
    lw t5, 76(sp)
    lw t6, 80(sp)
    lw a1, 84(sp)
    lw a2, 88(sp)
    lw a3, 92(sp)
    lw a4, 96(sp)
    lw a5, 100(sp)
    lw a6, 104(sp)
    lw a7, 108(sp)
    mv t0, a0
    mv t1, t0
    sub t0, s4, t1
    snez t0, t0
    beq x0, t0, _L4
    lw t0, 52(sp)
    mv a0, t0
    j main_exit
_L4:
_L2:
    li t0, 1
    lw t1, 52(sp)
    add t2, t1, t0
    mv t1, t2
    sw t1, 52(sp)
    j _L1
_L3:
    li t0, 100
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    lw s1, 0(sp)
    lw s2, 4(sp)
    lw s3, 8(sp)
    lw s4, 12(sp)
    lw ra, 44(sp)
    lw fp, 48(sp)
    addi sp, sp, 120
    # end of epilogue
    
    ret
    

