## Stage-4 实验报告

> 沙之洲 2020012408

### Step 9

#### 实验内容

step 9 的实际实验内容非常多且琐碎。这里只展示一些重要的部分，具体的细节可以看代码实现。

首先在 parse 部分，我们要支持函数的声明和定义，此二者的区别在于是否有函数体。这里我在 Function 这个 Node 节点上进行了区分

![image-20221204210552683](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221204210552683.png)

接下来我们需要在 namer 和 tacgen 部分不仅仅是对 main 函数进行访问，而是要对于每一个 function 进行访问。这里我们以 namer 为例进行展示

![image-20221204211057813](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221204211057813.png)

对于后端部分，我们需要做的主要是对于函数调用中 caller save 和 callee save 的处理

对于 caller save，这一部分的实现是在 bruteallocate 文件中，在 save caller save 之后，进行了函数传参

![image-20221204211317777](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221204211317777.png)

对于 callee save，是在 riscvasmemitter 中实现的。

![image-20221204211410285](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221204211410285.png)

由于我的函数读取参数是基于 FP 的，所以在 FP 也会在被调用函数执行的时候改变，因此也要作为 callee save reg 存在栈上。



#### 思考题

##### 1 不同参数的求值顺序会导致不同的返回结果

```c++
int f(int a, int b){
    return a;
}

int main(){
    int c = 0;
    return f(c += 1, c += 1)
}
```

如果是从左到右求值，返回结果会是 1 ，如果是从右到左求值，返回结果是 2

##### 2 为何 RISC-V 标准调用约定中要引入 callee-saved 和 caller-saved 两类寄存器，而不是要求所有寄存器完全由 caller/callee 中的一方保存？为何保存返回地址的 ra 寄存器是 caller-saved 寄存器？

由于将寄存器的值保存到栈上实际上涉及到了 memory 的操作，耗时较长。所以要尽可能在函数调用的时候减少这种向栈上存储的行为。

直观上理解，caller save 的意思就是这些寄存器不建议 caller 使用，因为一旦使用就需要在调用函数的时候将这些寄存器保存到栈上。同理对于 callee save 寄存器的意思也是不建议 callee 使用。通过让 caller 使用 callee save 的寄存器，callee 使用 caller save 的寄存器，能够在最大程度上减少函数调用的时候向栈上保存寄存器值的操作，从而提升程序的效率。

对于 ra 寄存器，实际上 ra 寄存器永远是指向当前正在执行的指令的地址。如果 ra 是 callee save 的，那么在函数调用的时候，会在函数跳转之后才保存 ra，但是这个时候 caller 正在执行的地址已经被覆盖了，这样会导致函数结束的 ret 不能返回到正确的位置。因此，ra 寄存器必然是 caller save 的。



### Step 10

#### 实验内容

对于本部分，我们首先需要在 parse 实现对于 global var 的解析

![image-20221204211526799](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221204211526799.png)

同理我们需要在 namer 和 tac gen 的时候首先处理 global var，这里和 function 的处理类似，不再赘述。

这里需要注意的是，当我们访问 global var 的时候，需要先找到 global var 的地址，再用 lw 来访问 global var 的值。这一步我是在 tac gen 中就实现了

![image-20221204211736767](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221204211736767.png)

接下来在后端只需要根据对应的 tac 指令去翻译即可。



#### 思考题

我们规定 inter = a - pc 。这里 pc 指的是当前指令的地址。则对于指令

```
la v0, a
```

会被翻译成

```
auipc t0, inter[31:12]
addi t0, t0, inter[11:0]
```

也有可能翻译成

```
auipc t0, inter[31:12]
ori t0, t0, inter[11:0]
```

