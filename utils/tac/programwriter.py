from __future__ import annotations

from typing import Any, Optional, Union

from utils.label.funclabel import *
from utils.label.label import Label, LabelKind

from .context import Context
from .funcvisitor import FuncVisitor
from .tacprog import TACProg

from frontend.ast.tree import Function


class ProgramWriter:
    def __init__(self, funcs: list[Function]) -> None:
        self.funcs = []
        self.ctx = Context()
        for func in funcs:
            funct_name = func.ident.value
            self.funcs.append(func)
            self.ctx.putFuncLabel(funct_name, len(func.parameter_list))

        self.global_vars = []

    def visitMainFunc(self) -> FuncVisitor:
        entry = MAIN_LABEL
        return FuncVisitor(entry, 0, self.ctx)

    def visitFunc(self, name: str, numArgs: int) -> FuncVisitor:
        entry = self.ctx.getFuncLabel(name)
        return FuncVisitor(entry, numArgs, self.ctx)

    def visitEnd(self) -> TACProg:
        return TACProg(self.ctx.funcs, self.global_vars)
