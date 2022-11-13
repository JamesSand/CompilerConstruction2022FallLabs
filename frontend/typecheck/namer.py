from typing import Protocol, TypeVar, cast

from frontend.ast.node import Node, NullType
from frontend.ast.tree import *
from frontend.ast.visitor import RecursiveVisitor, Visitor
from frontend.scope.globalscope import GlobalScope
from frontend.scope.scope import Scope, ScopeKind
from frontend.scope.scopestack import ScopeStack
from frontend.symbol.funcsymbol import FuncSymbol
from frontend.symbol.symbol import Symbol
from frontend.symbol.varsymbol import VarSymbol
from frontend.type.array import ArrayType
from frontend.type.type import DecafType
from utils.error import *
from utils.riscv import MAX_INT

"""
The namer phase: resolve all symbols defined in the abstract syntax tree and store them in symbol tables (i.e. scopes).
"""

# construct symbol table

# 构建符号
# 作用于屏蔽
# 名字查找


class Namer(Visitor[ScopeStack, None]): # basic class of any AST scanner
    def __init__(self) -> None:
        pass

    # Entry of this phase
    def transform(self, program: Program) -> Program: # entrance of the scan
        # Global scope. You don't have to consider it until Step 9.
        program.globalScope = GlobalScope
        ctx = ScopeStack(program.globalScope)

        program.accept(self, ctx)
        return program

    def visitProgram(self, program: Program, ctx: ScopeStack) -> None:
        # Check if the 'main' function is missing
        if not program.hasMainFunc():
            raise DecafNoMainFuncError

        # get all functions
        function_dict = program.functions()
        for funct_name, funct in function_dict.items():
            # visit each function
            funct.accept(self, ctx)
        
        # we can always visit the main function in the end
        # if have main function, then visit main function 
        # program.mainFunc().accept(self, ctx)

    def visitFunction(self, func: Function, ctx: ScopeStack) -> None:
        # check if it has declared
        funct_name = func.ident.value
        funct_type = func.ret_t.type
        if ctx.findConflict(funct_name):
            raise DecafDeclConflictError(funct_name)

        # declare the function
        funct_scope = Scope(ScopeKind.LOCAL)
        funct_symbol = FuncSymbol(funct_name, funct_type, funct_scope)
        ctx.declare(funct_symbol)

        # visit its parameters
        parameter_list = func.parameter_list
        for parameter in parameter_list:
            parameter.accept(self, ctx)

        # visit its body
        func.body.accept(self, ctx) # then visit the block of the function, recursively

    def visitBlock(self, block: Block, ctx: ScopeStack) -> None:
        # a function block is constructed by several sentence, we should visit all of them
        
        # we have to define a scope for each block 
        # open a scope here
        ctx.open(Scope(ScopeKind.LOCAL))

        for child in block:
            child.accept(self, ctx)

        # close the scope
        ctx.close()

    def visitReturn(self, stmt: Return, ctx: ScopeStack) -> None:
        stmt.expr.accept(self, ctx) # deal with the expression of return 

        """
        def visitFor(self, stmt: For, ctx: ScopeStack) -> None:

        1. Open a local scope for stmt.init.
        2. Visit stmt.init, stmt.cond, stmt.update.
        3. Open a loop in ctx (for validity checking of break/continue)
        4. Visit body of the loop.
        5. Close the loop and the local scope.
        """

    def visitIf(self, stmt: If, ctx: ScopeStack) -> None:
        stmt.cond.accept(self, ctx)
        stmt.then.accept(self, ctx)

        # check if the else branch exists
        if not stmt.otherwise is NULL:
            stmt.otherwise.accept(self, ctx)

    def visitWhile(self, stmt: While, ctx: ScopeStack) -> None:
        stmt.cond.accept(self, ctx)
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()

        """
        def visitDoWhile(self, stmt: DoWhile, ctx: ScopeStack) -> None:

        1. Open a loop in ctx (for validity checking of break/continue)
        2. Visit body of the loop.
        3. Close the loop.
        4. Visit the condition of the loop.
        """

    def visitDoWhile(self, stmt: DoWhile, ctx: ScopeStack) -> None:
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()
        stmt.cond.accept(self, ctx)

    def visitFor(self, stmt: For, ctx: ScopeStack) -> None:
        for_scope = Scope(ScopeKind.LOCAL)
        ctx.open(for_scope)
        stmt.init.accept(self, ctx)
        stmt.cond.accept(self, ctx)
        stmt.update.accept(self, ctx)
        
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()

        ctx.close()


    def visitContinue(self, stmt: Continue, ctx: ScopeStack) -> None:
        if not ctx.inLoop():
            raise DecafContinueOutsideLoopError()

    def visitBreak(self, stmt: Break, ctx: ScopeStack) -> None:
        if not ctx.inLoop():
            raise DecafBreakOutsideLoopError()

        # def visitContinue(self, stmt: Continue, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBreak.
        """

    def visitDeclaration(self, decl: Declaration, ctx: ScopeStack) -> None:
        """
        1. Use ctx.findConflict to find if a variable with the same name has been declared.
        2. If not, build a new VarSymbol, and put it into the current scope using ctx.declare.
        3. Set the 'symbol' attribute of decl.
        4. If there is an initial value, visit it.
        """

        # you have to read the defination carefully 
        name = decl.ident.value
        type = decl.var_t.type
        init_expr = decl.init_expr

        conflict_result = ctx.findConflict(name)
        if conflict_result:
            # conflict 
            raise DecafDeclConflictError(name)
        else:
            # no conflict
            new_decalre = VarSymbol(name, type)
            ctx.declare(new_decalre)
            # decl.ident.setattr('symbol', new_decalre)
            decl.setattr('symbol', new_decalre)
            
            # init value
            if not init_expr is NULL:
                # have init value, visit it 
                init_expr.accept(self, ctx)



    def visitAssignment(self, expr: Assignment, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBinary.
        """

        # minidecaf 不用考虑左右访问顺序
        # a[++i] = ++i;

        # 构建符号，访问即可

        expr.rhs.accept(self, ctx)
        expr.lhs.accept(self, ctx)
        
            

    def visitUnary(self, expr: Unary, ctx: ScopeStack) -> None:
        expr.operand.accept(self, ctx)

    def visitBinary(self, expr: Binary, ctx: ScopeStack) -> None:
        # since Binary have to operand, we have to visit all of them
        expr.lhs.accept(self, ctx)
        expr.rhs.accept(self, ctx)

    def visitCondExpr(self, expr: ConditionExpression, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBinary.
        """

        # a = t ? b : c
        # since cond_expr must have a otherwise branch

        expr.cond.accept(self, ctx)
        expr.then.accept(self, ctx)
        expr.otherwise.accept(self, ctx)

    def visitIdentifier(self, ident: Identifier, ctx: ScopeStack) -> None:
        """
        1. Use ctx.lookup to find the symbol corresponding to ident.
        2. If it has not been declared, raise a DecafUndefinedVarError.
        3. Set the 'symbol' attribute of ident.
        """
        # name = str(ident)
        name = ident.value
        lookup_result = ctx.lookup(name)
        if lookup_result is NULL:
            # not declare
            raise DecafUndefinedVarError(name)
        else:
            # declared
            # 所有作用域都在 namer 中使用并销毁，namer 结束之后，作用域的歧义将被消除
            # 由于 tacgen 会给以每个变量分配一个虚拟寄存器，
            # 所以需要将 varsymbol 挂载到 Identifier 上 
            ident.setattr('symbol', lookup_result) 

    def visitIntLiteral(self, expr: IntLiteral, ctx: ScopeStack) -> None:
        value = expr.value
        if value > MAX_INT: # check if the Int may overflow
            raise DecafBadIntValueError(value)


    # step9 codes below
    def visitParameter(self, parameter: Parameter, ctx: ScopeStack) -> None:
        # fine conflict in current scope
        param_name = parameter.ident.value
        param_type = parameter.var_t.type

        if ctx.findConflict(param_name):
            raise DecafDeclConflictError(param_name)

        # if no conflict, define a symbol for it and attach it on ast tree
        param_symbol = VarSymbol(param_name, param_type)
        parameter.setattr("symbol", param_symbol)
        

    def visitCall(self, call: Call, ctx: ScopeStack) -> None:
        # check if the function has defined
        funct_name = call.ident.value
        funct_to_call = ctx.lookup(funct_name)
        if not funct_to_call:
            raise DecafUndefinedVarError(funct_name)

        # check arguments number

        # check arguments type
        # do not need to do in this step


        pass
