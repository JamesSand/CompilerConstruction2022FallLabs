    .text
    .global main
    
main:
    # start of prologue
    
    # next local offset = 56 = 4 * 11 + 4 + 4 * 1
    addi sp, sp, -56
    sw ra, 44(sp)
    # end of prologue
    
    # start of body
    li t0, 5
    mv t1, t0

    # save caller save
    sw t0, 48(sp)
    sw t1, 52(sp)

    # pass parameter
    addi sp, sp, -4
    sw t1, 0(sp)

    # call fib function
    call fib

    # restore param stack
    addi sp, sp, 4

    # restore caller save
    lw t0, 48(sp)
    lw t1, 52(sp)

    # get function result
    mv t0, a0

    # return as main return
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    lw ra, 44(sp)
    addi sp, sp, 56
    # end of epilogue
    
    ret
    
fib:
    # start of prologue
    # 76 = 4 * 11 + 4 + 4 * 15 + 4 * 4
    addi sp, sp, -76
    sw ra, 44(sp)
    # end of prologue
    
    # start of body
    li t0, 0

    # load n to t1
    lw t1, 48(sp)

    # n == 0
    sub t2, t1, t0
    seqz t2, t2

    # n == 1
    li t0, 1
    sub t3, t1, t0
    seqz t3, t3

    # n == 0 || n == 1
    or t0, t2, t3
    snez t0, t0

    # store n
    sw t1, 48(sp)

    # if_condition
    beq x0, t0, _L1

    # here is wrong
    lw t0, 52(sp)
    mv a0, t0
    j fib_exit
_L1:
    li t0, 1
    lw t1, 52(sp)
    sub t2, t1, t0
    sw t0, 52(sp)
    sw t1, 48(sp)
    sw t2, 56(sp)
    sw t3, 60(sp)
    addi sp, sp, -4
    sw t2, 0(sp)
    call fib
    addi sp, sp, 4
    lw t0, 52(sp)
    lw t1, 64(sp)
    lw t2, 56(sp)
    lw t3, 60(sp)
    mv t0, a0
    li t2, 2
    sub t3, t1, t2
    sw t0, 64(sp)
    sw t1, 48(sp)
    sw t2, 68(sp)
    sw t3, 72(sp)
    addi sp, sp, -4
    sw t3, 0(sp)
    call fib
    addi sp, sp, 4
    lw t0, 64(sp)
    lw t1, 76(sp)
    lw t2, 68(sp)
    lw t3, 72(sp)
    mv t1, a0
    add t2, t0, t1
    mv a0, t2
    j fib_exit
    # end of body
    
fib_exit:
    # start of epilogue
    lw ra, 44(sp)
    addi sp, sp, 76
    # end of epilogue
    
    ret
    

