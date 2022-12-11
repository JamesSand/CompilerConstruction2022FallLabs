from typing import Protocol, TypeVar

from frontend.ast.node import Node
from frontend.ast.tree import *
from frontend.ast.visitor import Visitor
from frontend.scope.globalscope import GlobalScope
from frontend.scope.scope import Scope
from frontend.type.array import ArrayType
from utils.error import *
from frontend.symbol.varsymbol import VarSymbol

from frontend.type.builtin_type import INT, ARRAY

"""
The typer phase: type check abstract syntax tree.
"""

# symbol check
# scan AST tree and complete their task 
# from step 1 - 10, minidecaf only has type Int, do not need type check 


class Typer(Visitor[None, None]):
    def __init__(self) -> None:
        pass

    # Entry of this phase
    def transform(self, program: Program) -> Program:
        # here we donot need scope any more
        program.accept(self, None)
        return program

    def visitProgram(self, program: Program, ctx : None) -> None:
        # funct_list including global vars and functions
        # namely, here we may visit function or declaration 
        for item in program.funct_list:
            item.accept(self, ctx)


    def visitFunction(self, func: Function, ctx: None) -> None:
        # visit parameter
        for param in func.parameter_list:
            param.accept(self, ctx)
        # visit body
        func.body.accept(self, ctx)

    def visitBlock(self, block: Block, ctx: None) -> None:
        for child in block.children:
            child.accept(self, ctx)

    def visitReturn(self, stmt: Return, ctx: None) -> None:
        stmt.expr.accept(self, ctx)
        if stmt.expr.type != INT:
            raise TypeError("Return type is not IntType")

    def visitIf(self, stmt: If, ctx: None) -> None:
        stmt.cond.accept(self, ctx)
        if stmt.cond.type != INT:
            raise TypeError("If condition type is not IntType")
        stmt.then.accept(self, ctx)
        stmt.otherwise.accept(self, ctx)
        

    def visitWhile(self, stmt: While, ctx: None) -> None:
        stmt.cond.accept(self, ctx)
        if stmt.cond.type is not INT:
            raise TypeError("While condition type is not IntType")
        stmt.body.accept(self, ctx)
        

    def visitDoWhile(self, stmt: DoWhile, ctx: None) -> None:
        stmt.body.accept(self, ctx)
        stmt.cond.accept(self, ctx)
        if stmt.cond.type is not INT:
            raise TypeError("DoWhile condition type is not IntType")

    def visitFor(self, stmt: For, ctx: None) -> None:
        stmt.init.accept(self, ctx)
        stmt.cond.accept(self, ctx)
        if stmt.cond is not NULL and stmt.cond.type is not INT:
            raise TypeError("For condition type is not IntType")
        stmt.update.accept(self, ctx)
        stmt.body.accept(self, ctx)


    def visitContinue(self, stmt: Continue, ctx: None) -> None:
        pass

    def visitBreak(self, stmt: Break, ctx: None) -> None:
        pass

    def visitDeclaration(self, decl: Declaration, ctx: None) -> None:
        if decl.init_expr is not NULL:
            decl.init_expr.accept(self, ctx)
            if decl.init_expr.type != INT:
                raise TypeError("Declaration type is not IntType")



    def visitAssignment(self, expr: Assignment, ctx: None) -> None:
        expr.lhs.accept(self, ctx)
        if expr.lhs.type != INT:
            raise TypeError("Assignment left type is not IntType")
        
        expr.rhs.accept(self, ctx)
        if expr.rhs.type != INT:
            raise TypeError("Assignment right type is not IntType")

        expr.type = INT

    def visitUnary(self, expr: Unary, ctx: None) -> None:
        expr.operand.accept(self, ctx)
        if not expr.operand.type is INT:
            raise TypeError("Unary type is not IntType")
        expr.type = INT

    def visitBinary(self, expr: Binary, ctx: None) -> None:
        expr.lhs.accept(self, ctx)
        if expr.lhs.type != INT:
            raise TypeError("Binary left type is not IntType")

        expr.rhs.accept(self, ctx)
        if expr.rhs.type != INT:
            raise TypeError("Binary right type is not IntType")
        expr.type = INT

    def visitCondExpr(self, expr: ConditionExpression, ctx: None) -> None:
        expr.cond.accept(self, ctx)
        if expr.cond.type != INT:
            raise TypeError("Condition type is not IntType")

        expr.then.accept(self, ctx)
        if expr.then.type != INT:
            raise TypeError("Then type is not IntType")

        expr.otherwise.accept(self, ctx)
        if expr.otherwise.type != INT:
            raise TypeError("Otherwise type is not IntType")
        
        expr.type = INT

    def visitIdentifier(self, ident: Identifier, ctx: None) -> None:
        symbol : VarSymbol = ident.getattr("symbol")
        if len(symbol.size_list):
            ident.type = ARRAY
        else:
            ident.type = INT

    def visitIntLiteral(self, expr: IntLiteral, ctx: None) -> None:
        expr.type = INT


    # step9 codes below
    def visitParameter(self, parameter: Parameter, ctx: None) -> None:
        pass
        

    def visitCall(self, call: Call, ctx: None) -> None:
        call.type = INT

    def visitRefer(self, refer: Refer, ctx: None) -> None:
        refer.ident.accept(self, ctx)
        refer.type = refer.ident.type

        if len(refer.argument_list):
            # array call
            if refer.ident.type == INT:
                raise TypeError("Array call on non-array type")
            
            if refer.ident.type == ARRAY:
                # if len(refer.argument_list) != len(refer.ident.type.size_list):
                #     raise TypeError("Array call dimension mismatch")
                for arg in refer.argument_list:
                    arg.accept(self, ctx)
                    if arg.type != INT:
                        raise TypeError("Array call index is not IntType")

                refer.type = INT
                return
