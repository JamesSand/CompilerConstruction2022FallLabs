## Stage-3 实验报告

> 沙之洲 2020012408

### Step 7

#### 实验内容

在这一阶段，我们需要支持局部作用域。具体来说，要在 visitBlock 的时候打开一个新的作用域，namer.py 的代码如下

![image-20221202151044321](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221202151044321.png)

对于后端而言，这一阶段我们要考虑寄存器的分配。我们知道中间代码 tac 可以根据一些规则分为若干个 basic block ，这里 bruteallocate 实现的策略是对于每一个 bb 重新分配寄存器，因此我们要做的是只给那些程序可能能到达的 bb 分配寄存器，也就是那些可达的 bb，这里我才用的是 dfs 判断是否可达，具体代码如下

![image-20221202151326620](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221202151326620.png)



#### 思考题

控制流图如下

![image-20221205121846305](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221205121846305.png)


### Step 8

#### 实验内容

首先我们需要在解析 ast 树的时候增加 for 和 do while 的解析，代码如下

![image-20221202161841803](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221202161841803.png)

接下来需要在前端的 namer 和 tacgen 的对应部分增加对应的 visit 函数，这里以 tacgen 中的 visitFor 为例

![image-20221202161945169](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221202161945169.png)

在 visit 函数中需要做的操作包括，打开局部作用域，指定标签等。



#### 思考题

![image-20221202162754045](C:\Users\James\AppData\Roaming\Typora\typora-user-images\image-20221202162754045.png)

首先给出结论：第二种翻译方式使用的指令条数更少，因此第二种翻译方式更好。

原因如下：

可以看到第一种和第二种翻译方式的区别主要在于，第一种翻译方式是在进入 body 之前进行  condition 的判断，也就是说，每次 body 结束之后，都需要一个无条件的跳转，才能开始下一轮的 condition 的判断和迭代。但是对于第二种翻译方式，将跳转和 condition 判断这两步操作放到同一条指令中进行，也就是第 7 条的 bnez BEGIN_LABEL 指令。

不难看出，对于每一轮迭代，第一种翻译方式都会比第二种翻译方式多执行一条指令。因此，第二种翻译方式更好。
