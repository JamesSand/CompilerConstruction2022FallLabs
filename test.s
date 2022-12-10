    .data
    .global n
n:
    .word 5
    .bss
    .global a
a:
    .space 20
    .data
    .global state
state:
    .word 0
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
    addi sp, sp, -96
    sw ra, 44(sp)
    sw fp, 48(sp)
    addi fp, sp, 96
    # end of prologue
    
    # start of body
    la t0, n
    lw t1, 0(t0)
    sw t0, 52(sp)
    sw t1, 56(sp)
    lw a0, 56(sp)
    call initArr
    lw t0, 52(sp)
    lw t1, 56(sp)
    mv t0, a0
    la t0, n
    lw t1, 0(t0)
    sw t0, 60(sp)
    sw t1, 64(sp)
    lw a0, 64(sp)
    call isSorted
    lw t0, 60(sp)
    lw t1, 64(sp)
    mv t0, a0
    mv t1, t0
    li t0, 0
    la t2, n
    lw t3, 0(t2)
    li t2, 1
    sub t4, t3, t2
    sw t0, 68(sp)
    sw t1, 72(sp)
    sw t2, 76(sp)
    sw t3, 80(sp)
    sw t4, 84(sp)
    lw a0, 68(sp)
    lw a1, 84(sp)
    call qsort
    lw t0, 68(sp)
    lw t1, 72(sp)
    lw t2, 76(sp)
    lw t3, 80(sp)
    lw t4, 84(sp)
    mv t0, a0
    la t0, n
    lw t2, 0(t0)
    sw t0, 88(sp)
    sw t1, 72(sp)
    sw t2, 92(sp)
    sw t3, 80(sp)
    sw t4, 84(sp)
    lw a0, 92(sp)
    call isSorted
    lw t0, 88(sp)
    lw t1, 72(sp)
    lw t2, 92(sp)
    lw t3, 80(sp)
    lw t4, 84(sp)
    mv t0, a0
    mv t2, t0
    li t0, 0
    sub t3, t1, t0
    seqz t3, t3
    li t0, 1
    sub t1, t2, t0
    seqz t1, t1
    snez t0, t3
    and t0, t0, t1
    snez t0, t0
    seqz t1, t0
    beq x0, t1, _L1
    li t0, 1
    mv a0, t0
    j main_exit
_L1:
    li t0, 0
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    lw ra, 44(sp)
    lw fp, 48(sp)
    addi sp, sp, 96
    addi sp, sp, 32
    # end of epilogue
    
    ret
    
qsort:
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
    addi sp, sp, -96
    sw ra, 44(sp)
    sw fp, 48(sp)
    addi fp, sp, 96
    # end of prologue
    
    # start of body
    lw t0, 0(fp)
    mv t1, t0
    lw t2, 4(fp)
    mv t3, t2
    la t4, a
    add t5, t0, t2
    li t6, 2
    div a1, t5, t6
    li t5, 0
    li t6, 1
    mul a2, a1, t6
    add t5, t5, a2
    li t6, 4
    mul t5, t5, t6
    add t5, t5, t4
    lw t4, 0(t5)
    mv t5, t4
    li t4, 1
    mv t6, t4
    sw t0, 52(sp)
    sw t2, 56(sp)
    sw t1, 60(sp)
    sw t3, 64(sp)
    sw t5, 68(sp)
_L2:
    lw t0, 60(sp)
    lw t1, 64(sp)
    sgt t2, t0, t1
    seqz t2, t2
    sw t0, 60(sp)
    sw t1, 64(sp)
    beq x0, t2, _L4
_L5:
    la t0, a
    li t1, 0
    li t2, 1
    lw t3, 60(sp)
    mul t4, t3, t2
    add t1, t1, t4
    li t2, 4
    mul t1, t1, t2
    add t1, t1, t0
    lw t0, 0(t1)
    lw t1, 68(sp)
    slt t2, t0, t1
    sw t3, 60(sp)
    sw t1, 68(sp)
    beq x0, t2, _L7
    li t0, 1
    lw t1, 60(sp)
    add t2, t1, t0
    mv t1, t2
    sw t1, 60(sp)
_L6:
    j _L5
_L7:
_L8:
    la t0, a
    li t1, 0
    li t2, 1
    lw t3, 64(sp)
    mul t4, t3, t2
    add t1, t1, t4
    li t2, 4
    mul t1, t1, t2
    add t1, t1, t0
    lw t0, 0(t1)
    lw t1, 68(sp)
    sgt t2, t0, t1
    sw t3, 64(sp)
    sw t1, 68(sp)
    beq x0, t2, _L10
    li t0, 1
    lw t1, 64(sp)
    sub t2, t1, t0
    mv t1, t2
    sw t1, 64(sp)
_L9:
    j _L8
_L10:
    lw t0, 60(sp)
    lw t1, 64(sp)
    sgt t2, t0, t1
    sw t0, 60(sp)
    sw t1, 64(sp)
    beq x0, t2, _L11
    j _L4
_L11:
    la t0, a
    li t1, 0
    li t2, 1
    lw t3, 60(sp)
    mul t4, t3, t2
    add t1, t1, t4
    li t2, 4
    mul t1, t1, t2
    add t1, t1, t0
    lw t0, 0(t1)
    mv t1, t0
    la t0, a
    li t2, 0
    li t4, 1
    lw t5, 64(sp)
    mul t6, t5, t4
    add t2, t2, t6
    li t4, 4
    mul t2, t2, t4
    add t2, t2, t0
    lw t0, 0(t2)
    la t2, a
    li t4, 0
    li t6, 1
    mul a1, t3, t6
    add t4, t4, a1
    li t6, 4
    mul t4, t4, t6
    add t4, t4, t2
    lw t2, 0(t4)
    mv t2, t0
    sw t2, 0(t4)
    la t0, a
    li t2, 0
    li t4, 1
    mul t6, t5, t4
    add t2, t2, t6
    li t4, 4
    mul t2, t2, t4
    add t2, t2, t0
    lw t0, 0(t2)
    mv t0, t1
    sw t0, 0(t2)
    li t0, 1
    add t1, t3, t0
    mv t3, t1
    li t0, 1
    sub t1, t5, t0
    mv t5, t1
    sw t3, 60(sp)
    sw t5, 64(sp)
_L3:
    j _L2
_L4:
    lw t0, 60(sp)
    lw t1, 4(fp)
    slt t2, t0, t1
    sw t1, 56(sp)
    sw t0, 60(sp)
    beq x0, t2, _L12
    lw t0, 60(sp)
    lw t1, 4(fp)
    sw t0, 60(sp)
    sw t1, 56(sp)
    sw t2, 72(sp)
    sw t3, 60(sp)
    sw t4, 76(sp)
    sw t5, 64(sp)
    sw t6, 80(sp)
    sw a1, 84(sp)
    sw a2, 88(sp)
    lw a0, 60(sp)
    lw a1, 56(sp)
    call qsort
    lw t0, 60(sp)
    lw t1, 4(fp)
    lw t2, 72(sp)
    lw t3, 60(sp)
    lw t4, 76(sp)
    lw t5, 64(sp)
    lw t6, 80(sp)
    lw a1, 84(sp)
    lw a2, 88(sp)
    mv t0, a0
_L12:
    lw t0, 64(sp)
    lw t1, 0(fp)
    sgt t2, t0, t1
    sw t1, 52(sp)
    sw t0, 64(sp)
    beq x0, t2, _L13
    lw t0, 0(fp)
    lw t1, 64(sp)
    sw t0, 52(sp)
    sw t1, 64(sp)
    sw t2, 92(sp)
    sw t3, 60(sp)
    sw t4, 76(sp)
    sw t5, 64(sp)
    sw t6, 80(sp)
    sw a1, 84(sp)
    sw a2, 88(sp)
    lw a0, 52(sp)
    lw a1, 64(sp)
    call qsort
    lw t0, 0(fp)
    lw t1, 64(sp)
    lw t2, 92(sp)
    lw t3, 60(sp)
    lw t4, 76(sp)
    lw t5, 64(sp)
    lw t6, 80(sp)
    lw a1, 84(sp)
    lw a2, 88(sp)
    mv t0, a0
_L13:
    li a0, 0
    j qsort_exit
    # end of body
    
qsort_exit:
    # start of epilogue
    lw ra, 44(sp)
    lw fp, 48(sp)
    addi sp, sp, 96
    addi sp, sp, 32
    # end of epilogue
    
    ret
    
rand:
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
    la t0, state
    lw t1, 0(t0)
    li t0, 64013
    mul t2, t1, t0
    li t0, 1531011
    add t1, t2, t0
    li t0, 32768
    rem t2, t1, t0
    la t0, state
    lw t1, 0(t0)
    mv t1, t2
    la t0, state
    sw t1, 0(t0)
    la t0, state
    lw t1, 0(t0)
    li t0, 1000
    rem t2, t1, t0
    mv a0, t2
    j rand_exit
    # end of body
    
rand_exit:
    # start of epilogue
    lw ra, 44(sp)
    lw fp, 48(sp)
    addi sp, sp, 52
    addi sp, sp, 32
    # end of epilogue
    
    ret
    
initArr:
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
    addi sp, sp, -84
    sw ra, 44(sp)
    sw fp, 48(sp)
    addi fp, sp, 84
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    sw t1, 52(sp)
_L14:
    lw t0, 52(sp)
    lw t1, 0(fp)
    slt t2, t0, t1
    sw t1, 56(sp)
    sw t0, 52(sp)
    beq x0, t2, _L16
    sw t0, 52(sp)
    sw t1, 56(sp)
    sw t2, 60(sp)
    sw t3, 64(sp)
    sw t4, 68(sp)
    sw t5, 60(sp)
    sw t6, 72(sp)
    sw a1, 76(sp)
    sw a2, 80(sp)
    call rand
    lw t0, 52(sp)
    lw t1, 0(fp)
    lw t2, 60(sp)
    lw t3, 64(sp)
    lw t4, 68(sp)
    lw t5, 60(sp)
    lw t6, 72(sp)
    lw a1, 76(sp)
    lw a2, 80(sp)
    mv t0, a0
    la t1, a
    li t2, 0
    li t3, 1
    lw t4, 52(sp)
    mul t5, t4, t3
    add t2, t2, t5
    li t3, 4
    mul t2, t2, t3
    add t2, t2, t1
    lw t1, 0(t2)
    mv t1, t0
    sw t1, 0(t2)
    li t0, 1
    add t1, t4, t0
    mv t4, t1
    sw t4, 52(sp)
_L15:
    j _L14
_L16:
    li a0, 0
    j initArr_exit
    # end of body
    
initArr_exit:
    # start of epilogue
    lw ra, 44(sp)
    lw fp, 48(sp)
    addi sp, sp, 84
    addi sp, sp, 32
    # end of epilogue
    
    ret
    
isSorted:
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
    addi sp, sp, -60
    sw ra, 44(sp)
    sw fp, 48(sp)
    addi fp, sp, 60
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    sw t1, 52(sp)
_L17:
    li t0, 1
    lw t1, 0(fp)
    sub t2, t1, t0
    lw t0, 52(sp)
    slt t3, t0, t2
    sw t1, 56(sp)
    sw t0, 52(sp)
    beq x0, t3, _L19
    la t0, a
    li t1, 0
    li t2, 1
    lw t3, 52(sp)
    mul t4, t3, t2
    add t1, t1, t4
    li t2, 4
    mul t1, t1, t2
    add t1, t1, t0
    lw t0, 0(t1)
    la t1, a
    li t2, 1
    add t4, t3, t2
    li t2, 0
    li t5, 1
    mul t6, t4, t5
    add t2, t2, t6
    li t4, 4
    mul t2, t2, t4
    add t2, t2, t1
    lw t1, 0(t2)
    sgt t2, t0, t1
    sw t3, 52(sp)
    beq x0, t2, _L20
    li t0, 0
    mv a0, t0
    j isSorted_exit
_L20:
    li t0, 1
    lw t1, 52(sp)
    add t2, t1, t0
    mv t1, t2
    sw t1, 52(sp)
_L18:
    j _L17
_L19:
    li t0, 1
    mv a0, t0
    j isSorted_exit
    # end of body
    
isSorted_exit:
    # start of epilogue
    lw ra, 44(sp)
    lw fp, 48(sp)
    addi sp, sp, 60
    addi sp, sp, 32
    # end of epilogue
    
    ret
    

