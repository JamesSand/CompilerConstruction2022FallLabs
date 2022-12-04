import utils.riscv as riscv
from frontend.ast import node
from frontend.ast.tree import *
from frontend.ast.visitor import Visitor
from frontend.symbol.varsymbol import VarSymbol
from frontend.type.array import ArrayType

from utils.tac.tacinstr import Global
from utils.tac import tacop
from utils.tac.funcvisitor import FuncVisitor
from utils.tac.programwriter import ProgramWriter
from utils.tac.tacprog import TACProg
from utils.tac.temp import Temp

from frontend.symbol.funcsymbol import FuncSymbol


"""
The TAC generation phase: translate the abstract syntax tree into three-address code.
"""


class TACGen(Visitor[FuncVisitor, None]):
    def __init__(self) -> None:
        pass

    # Entry of this phase
    def transform(self, program: Program) -> TACProg:

        function_dict : dict [str , Function]= program.functions()
        funct_list = []
        for funct_name, funct in function_dict.items():
            funct_list.append(funct)

        pw = ProgramWriter(funct_list)

        # deal with global var first
        global_var : list[Declaration]= program.global_vars()
        for var in global_var:
            init_value = 0
            if var.init_expr is not NULL:
                init_value = var.init_expr.value
            
            pw.global_vars.append(Global(var.ident.value, init_value))


        funct_name_dict = {}

        for funct_name, funct in function_dict.items():
            if funct_name == "main":
                continue

            if funct.body is NULL:
                continue

            # open a function visitor
            parameter_list = funct.parameter_list
            parameter_num = len(parameter_list)
            mv : FuncVisitor = pw.visitFunc(funct_name, parameter_num)

            funct_symbol : FuncSymbol = funct.getattr("symbol")

            # visit parameter list
            for parameter in parameter_list:
                parameter_temp = parameter.accept(self, mv)
                # record which temps are need by this function
                funct_symbol.add_parameter_temp(parameter_temp)

            funct_name_dict[funct_name] = mv

        # here we can visit main in the end
        mainFunc = program.mainFunc()
        
        # The function visitor of 'main' is special.
        mv = pw.visitMainFunc()

        mainFunc.body.accept(self, mv)
        # Remember to call mv.visitEnd after the translation a function.
        mv.visitEnd()


        for funct_name, funct in function_dict.items():
            if funct_name == "main":
                continue

            if funct.body is NULL:
                continue

            mv = funct_name_dict[funct_name]

            # if funct.body is not NULL:
            funct.body.accept(self, mv)

            mv.visitEnd()

        # Remember to call pw.visitEnd before finishing the translation phase.
        return pw.visitEnd()
    

    def visitBlock(self, block: Block, mv: FuncVisitor) -> None:
        for child in block:
            child.accept(self, mv)

    def visitReturn(self, stmt: Return, mv: FuncVisitor) -> None:
        stmt.expr.accept(self, mv)
        mv.visitReturn(stmt.expr.getattr("val"))

    def visitBreak(self, stmt: Break, mv: FuncVisitor) -> None:
        # print("visit break")
        mv.visitBranch(mv.getBreakLabel())

    def visitContinue(self, stmt: Continue, mv: FuncVisitor) -> None:
        # print("continue")
        # print(mv.getContinueLabel())
        # with open("log.txt", "w") as fw:
        #     fw.write(str(mv.getContinueLabel()))
        mv.visitBranch(mv.getContinueLabel())

    def visitIdentifier(self, ident: Identifier, mv: FuncVisitor) -> None:
        """
        1. Set the 'val' attribute of ident as the temp variable of the 'symbol' attribute of ident.
        """
        symbol : VarSymbol= ident.getattr("symbol")
        if symbol is None:
            breakpoint()
        if symbol.isGlobal:
            var_name = symbol.name
            var_addr = mv.visitLoadGlobalAddr(var_name)
            var_temp = mv.visitLoadFromMem(var_addr, 0)
            ident.setattr("val", var_temp)
        else:
            temp = symbol.temp
            # Identifier 的挂载和 Declaration 的挂载一致
            ident.setattr("val", temp)

        # 先给 a 一个 虚拟寄存器

    def visitDeclaration(self, decl: Declaration, mv: FuncVisitor) -> None:
        """
        1. Get the 'symbol' attribute of decl.
        2. Use mv.freshTemp to get a new temp variable for this symbol.
        3. If the declaration has an initial value, use mv.visitAssignment to set it.
        """
        new_var = decl.getattr('symbol')
        new_var.temp = mv.freshTemp()
        init_expr = decl.init_expr
        if not init_expr is NULL:
            init_expr.accept(self, mv) # 翻译成三地址码指令
            value = init_expr.getattr("val") # 所有表达式都有一个值，三地址码左边的虚拟寄存器是 val
            mv.visitAssignment(new_var.temp, value) # 生成了一条三地址码的赋值语句

    def visitAssignment(self, expr: Assignment, mv: FuncVisitor) -> None:
        """
        1. Visit the right hand side of expr, and get the temp variable of left hand side.
        2. Use mv.visitAssignment to emit an assignment instruction.
        3. Set the 'val' attribute of expr as the value of assignment instruction.
        """

        # a = b = 1
        # 表达式的返回值是 左值的值

        expr.lhs.accept(self, mv)
        expr.rhs.accept(self, mv)

        # 右边的值赋给左边
        # 左边的值赋给表达式

        assign_result = mv.visitAssignment(expr.lhs.getattr("val"), expr.rhs.getattr("val"))

        # expression 的 val 是左值的 虚拟寄存器
        expr.setattr("val", assign_result)

        if isinstance(expr.lhs, Identifier):
            symbol : VarSymbol= expr.lhs.getattr("symbol")
            if symbol.isGlobal:
                var_name = symbol.name
                var_addr = mv.visitLoadGlobalAddr(var_name)
                mv.visitStoreToMem(expr.lhs.getattr("val"), 0, var_addr)

    def visitIf(self, stmt: If, mv: FuncVisitor) -> None:
        # visiti condition
        stmt.cond.accept(self, mv)

        if stmt.otherwise is NULL:
            # only have a if, do not have an else
            skipLabel = mv.freshLabel()
            mv.visitCondBranch(
                tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), skipLabel
            )
            stmt.then.accept(self, mv)
            mv.visitLabel(skipLabel)
        else:
            # have an else
            # define two labels, exit label for then, exitlabel for otherwise
            skipLabel = mv.freshLabel()
            exitLabel = mv.freshLabel()
            # add beq instruction
            mv.visitCondBranch(
                tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), skipLabel
            )
            # visit then expression
            stmt.then.accept(self, mv)
            # add exit label to then branch
            mv.visitBranch(exitLabel)

            mv.visitLabel(skipLabel)
            stmt.otherwise.accept(self, mv)

            mv.visitLabel(exitLabel)

    def visitWhile(self, stmt: While, mv: FuncVisitor) -> None:
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()
        mv.openLoop(breakLabel, loopLabel)

        mv.visitLabel(beginLabel)
        stmt.cond.accept(self, mv)
        # equal to zero then jump to break label
        mv.visitCondBranch(tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), breakLabel)

        stmt.body.accept(self, mv)
        # casue loop label is used as continue label, so put it here
        mv.visitLabel(loopLabel)
        mv.visitBranch(beginLabel)
        mv.visitLabel(breakLabel)
        mv.closeLoop()

    def visitDoWhile(self, stmt: DoWhile, mv: FuncVisitor) -> None:
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()

        mv.openLoop(breakLabel, loopLabel)

        mv.visitLabel(beginLabel)

        stmt.body.accept(self, mv)

        mv.visitLabel(loopLabel)
        stmt.cond.accept(self, mv)
        # equal to zero then jump to break label
        mv.visitCondBranch(tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), breakLabel)

        mv.visitBranch(beginLabel)

        mv.visitLabel(breakLabel)
        mv.closeLoop()

    def visitFor(self, stmt: For, mv: FuncVisitor) -> None:
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()

        if not isinstance(stmt.init, node.NullType):
            stmt.init.accept(self, mv)

        mv.openLoop(breakLabel, loopLabel)

        mv.visitLabel(beginLabel)
        
        if not isinstance(stmt.cond, node.NullType):
            stmt.cond.accept(self, mv)
            mv.visitCondBranch(tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), breakLabel)
        # stmt.cond.accept(self, mv)
        # mv.visitCondBranch(tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), breakLabel)

        stmt.body.accept(self, mv)

        mv.visitLabel(loopLabel)

        if not isinstance(stmt.update, node.NullType):
            stmt.update.accept(self, mv)
        mv.visitBranch(beginLabel)
        
        mv.visitLabel(breakLabel)
        mv.closeLoop()


    def visitUnary(self, expr: Unary, mv: FuncVisitor) -> None:
        expr.operand.accept(self, mv)

        op = {
            node.UnaryOp.Neg: tacop.UnaryOp.NEG,
            # You can add unary operations here.
            # step2
            # BitNot = ~ correspond to not
            node.UnaryOp.BitNot: tacop.UnaryOp.NOT,
            # LogicNot = ! correspond to seqz
            node.UnaryOp.LogicNot: tacop.UnaryOp.SEQZ
        }[expr.op]
        expr.setattr("val", mv.visitUnary(op, expr.operand.getattr("val")))

    def visitBinary(self, expr: Binary, mv: FuncVisitor) -> None:
        expr.lhs.accept(self, mv)
        expr.rhs.accept(self, mv)

        op = {
            node.BinaryOp.Add: tacop.BinaryOp.ADD,
            # You can add binary operations here.
            # step3
            # 加减乘除显然是容易实现的
            node.BinaryOp.Sub : tacop.BinaryOp.SUB,
            node.BinaryOp.Mul: tacop.BinaryOp.MUL,
            node.BinaryOp.Div : tacop.BinaryOp.DIV,
            # mod correspond to rem
            node.BinaryOp.Mod : tacop.BinaryOp.REM,

            # step4
            # LT = < 自带的
            node.BinaryOp.LT : tacop.BinaryOp.SLT,
            node.BinaryOp.GT : tacop.BinaryOp.SGT,
            # 要写的
            node.BinaryOp.EQ : tacop.BinaryOp.EQU,
            node.BinaryOp.NE : tacop.BinaryOp.NEQ,
            node.BinaryOp.LE : tacop.BinaryOp.LEQ,
            node.BinaryOp.GE : tacop.BinaryOp.GEQ,
            node.BinaryOp.LogicAnd :tacop.BinaryOp.AND,
            node.BinaryOp.LogicOr : tacop.BinaryOp.OR,

        }[expr.op]
        # 直接根据 expr.op 取字典里边的 op
        expr.setattr(
            "val", mv.visitBinary(op, expr.lhs.getattr("val"), expr.rhs.getattr("val"))
        )

    def visitCondExpr(self, expr: ConditionExpression, mv: FuncVisitor) -> None:
        """
        1. Refer to the implementation of visitIf and visitBinary.
        """
        # a = cond ? then : otherwise

        skipLabel = mv.freshLabel()
        exitLabel = mv.freshLabel()
        temp = mv.freshTemp()
        expr.setattr("val", temp)

        # visit condition
        expr.cond.accept(self, mv)
        mv.visitCondBranch(
            tacop.CondBranchOp.BEQ, expr.cond.getattr("val"), skipLabel
        )

        expr.then.accept(self, mv)
        mv.visitAssignment(temp, expr.then.getattr("val"))
        mv.visitBranch(exitLabel) # jump to exit

        mv.visitLabel(skipLabel)
        expr.otherwise.accept(self, mv)
        mv.visitAssignment(temp, expr.otherwise.getattr("val"))

        mv.visitLabel(exitLabel)


    def visitIntLiteral(self, expr: IntLiteral, mv: FuncVisitor) -> None:
        expr.setattr("val", mv.visitLoad(expr.value))


    def visitParameter(self, parameter: Parameter, mv: FuncVisitor) -> Temp:
        # allocate a temp for this parameter
        parameter_temp = mv.freshTemp()
        parameter_symbol = parameter.getattr("symbol")
        parameter_symbol.temp = parameter_temp
        return parameter_temp

    def visitCall(self, call : Call, mv: FuncVisitor) -> None:
        argument_list = call.argument_list

        # breakpoint()

        # if len(argument_list) == 3:
        #     breakpoint()

        argument_temp_list = []

        for argument in argument_list:
            # allocate temp for each argument, expression in actual
            # breakpoint()
            argument.accept(self, mv)
            # use param to declare arguments
            argument_temp = argument.getattr("val")

            # wait all calulate done then visit param temp
            argument_temp_list.append(argument_temp)
        
        for argument_temp in argument_temp_list:
            mv.visitParameter(argument_temp)

        # call the function
        funct_name = call.ident.value
        call_result_temp = mv.visitCall(funct_name)
        call.setattr("val", call_result_temp)
        
