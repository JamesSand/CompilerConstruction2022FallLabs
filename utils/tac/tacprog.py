from typing import Any, Optional, Union

from .tacfunc import TACFunc
from utils.tac.tacinstr import Global


# A TAC program consists of several TAC functions.
class TACProg:
    def __init__(self, funcs: list[TACFunc], global_vars : list[Global]) -> None:
        self.funcs = funcs
        self.global_vars = global_vars

    def printTo(self) -> None:
        for var in self.global_vars:
            print(f"{str(var)}")
        for func in self.funcs:
            func.printTo()
