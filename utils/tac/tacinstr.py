from enum import Enum, auto, unique
from typing import Any, Optional, Union

from utils.label.label import Label
from utils.tac.nativeinstr import NativeInstr
from utils.tac.reg import Reg

from .tacop import *
from .tacvisitor import TACVisitor
from .temp import Temp


class TACInstr:
    def __init__(
        self,
        kind: InstrKind,
        dsts: list[Temp],
        srcs: list[Temp],
        label: Optional[Label],
    ) -> None:
        self.kind = kind
        self.dsts = dsts.copy()
        self.srcs = srcs.copy()
        self.label = label

    def getRead(self) -> list[int]:
        ret_list = []
        for src in self.srcs:
            # if isinstance(src, int):
            #     breakpoint()
            ret_list.append(src.index)

        return ret_list
        # return [src.index for src in self.srcs]

    def getWritten(self) -> list[int]:
        return [dst.index for dst in self.dsts]

    def isLabel(self) -> bool:
        return self.kind is InstrKind.LABEL

    def isSequential(self) -> bool:
        return self.kind == InstrKind.SEQ

    def isReturn(self) -> bool:
        return self.kind == InstrKind.RET

    def toNative(self, dstRegs: list[Reg], srcRegs: list[Reg]) -> NativeInstr:
        oldDsts = dstRegs
        oldSrcs = srcRegs
        self.dsts = dstRegs
        self.srcs = srcRegs
        instrString = self.__str__()
        newInstr = NativeInstr(self.kind, dstRegs, srcRegs, self.label, instrString)
        self.dsts = oldDsts
        self.srcs = oldSrcs
        return newInstr

    def accept(self, v: TACVisitor) -> None:
        pass


# Assignment instruction.
class Assign(TACInstr):
    def __init__(self, dst: Temp, src: Temp) -> None:
        super().__init__(InstrKind.SEQ, [dst], [src], None)
        self.dst = dst
        self.src = src

    def __str__(self) -> str:
        return "%s = %s" % (self.dst, self.src)

    def accept(self, v: TACVisitor) -> None:
        v.visitAssign(self)


# Loading an immediate 32-bit constant.
class LoadImm4(TACInstr):
    def __init__(self, dst: Temp, value: int) -> None:
        super().__init__(InstrKind.SEQ, [dst], [], None)
        self.dst = dst
        self.value = value

    def __str__(self) -> str:
        return "%s = %d" % (self.dst, self.value)

    def accept(self, v: TACVisitor) -> None:
        v.visitLoadImm4(self)


# Unary operations.
class Unary(TACInstr):
    def __init__(self, op: UnaryOp, dst: Temp, operand: Temp) -> None:
        super().__init__(InstrKind.SEQ, [dst], [operand], None)
        self.op = op
        self.dst = dst
        self.operand = operand

    def __str__(self) -> str:
        return "%s = %s %s" % (
            self.dst,
            ("-" if (self.op == UnaryOp.NEG) else "!"),
            self.operand,
        )

    def accept(self, v: TACVisitor) -> None:
        v.visitUnary(self)


# Binary Operations.
class Binary(TACInstr):
    def __init__(self, op: BinaryOp, dst: Temp, lhs: Temp, rhs: Temp) -> None:
        super().__init__(InstrKind.SEQ, [dst], [lhs, rhs], None)
        self.op = op
        self.dst = dst
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        opStr = {
            BinaryOp.ADD: "+",
            BinaryOp.SUB: "-",
            BinaryOp.MUL: "*",
            BinaryOp.DIV: "/",
            BinaryOp.REM: "%",
            BinaryOp.EQU: "==",
            BinaryOp.NEQ: "!=",
            BinaryOp.SLT: "<",
            BinaryOp.LEQ: "<=",
            BinaryOp.SGT: ">",
            BinaryOp.GEQ: ">=",
            BinaryOp.AND: "&&",
            BinaryOp.OR: "||",
        }[self.op]
        return "%s = (%s %s %s)" % (self.dst, self.lhs, opStr, self.rhs)

    def accept(self, v: TACVisitor) -> None:
        v.visitBinary(self)


# Branching instruction.
class Branch(TACInstr):
    def __init__(self, target: Label) -> None:
        super().__init__(InstrKind.JMP, [], [], target)
        self.target = target

    def __str__(self) -> str:
        return "branch %s" % str(self.target)

    def accept(self, v: TACVisitor) -> None:
        v.visitBranch(self)


# Branching with conditions.
class CondBranch(TACInstr):
    def __init__(self, op: CondBranchOp, cond: Temp, target: Label) -> None:
        super().__init__(InstrKind.COND_JMP, [], [cond], target)
        self.op = op
        self.cond = cond
        self.target = target

    def __str__(self) -> str:
        return "if (%s %s) branch %s" % (
            self.cond,
            "== 0" if self.op == CondBranchOp.BEQ else "!= 0",
            str(self.target),
        )

    def accept(self, v: TACVisitor) -> None:
        v.visitCondBranch(self)


# Return instruction.
class Return(TACInstr):
    def __init__(self, value: Optional[Temp]) -> None:
        if value is None:
            super().__init__(InstrKind.RET, [], [], None)
        else:
            super().__init__(InstrKind.RET, [], [value], None)
        self.value = value

    def __str__(self) -> str:
        return "return" if (self.value is None) else ("return " + str(self.value))

    def accept(self, v: TACVisitor) -> None:
        v.visitReturn(self)


# Annotation (used for debugging).
class Memo(TACInstr):
    def __init__(self, msg: str) -> None:
        super().__init__(InstrKind.SEQ, [], [], None)
        self.msg = msg

    def __str__(self) -> str:
        return "memo '%s'" % self.msg

    def accept(self, v: TACVisitor) -> None:
        v.visitMemo(self)


# Label (function entry or branching target).
class Mark(TACInstr):
    def __init__(self, label: Label) -> None:
        super().__init__(InstrKind.LABEL, [], [], label)

    def __str__(self) -> str:
        return "%s:" % str(self.label)

    def accept(self, v: TACVisitor) -> None:
        v.visitMark(self)


# step 9 codes here
class Param(TACInstr):
    def __init__(self, parameter: Temp) -> None:
        super().__init__(InstrKind.SEQ, [parameter], [], None)
        self.parameter = parameter

    def __str__(self) -> str:
        return "PARAM %s" % (self.parameter)

    def accept(self, v: TACVisitor) -> None:
        return v.visitParameter(self)

class Call(TACInstr):
    def __init__(self,result : Temp, target: Label) -> None:
        super().__init__(InstrKind.SEQ, [result], [], target)
        self.result = result
        self.target = target

    def __str__(self) -> str:
        return "%s = CALL %s" % (str(self.result), str(self.target))

    def accept(self, v: TACVisitor) -> None:
        v.visitCall(self)

class Global(TACInstr):
    def __init__(self, name: str, size : int, is_array : bool, value : int) -> None:
        super().__init__(InstrKind.SEQ, [], [], None)
        self.name = name
        self.size = size
        self.array = is_array
        self.value = value

    def __str__(self) -> str:
        if self.array:
            return "GLOBAL Array name: %s size: %d" % (self.name,self.size)
        else:
            return "GLOBAL Var name: %s value: %d" % (self.name,self.value)

    def accept(self, v: TACVisitor) -> None:
        v.visitGlobal(self)

class LoadGlobalAddr(TACInstr):
    def __init__(self, dst: Temp, name: str) -> None:
        super().__init__(InstrKind.SEQ, [dst], [], None)
        self.dst = dst
        self.name = name

    def __str__(self) -> str:
        return "%s = GLOBAL_VAR %s" % (self.dsts[0], self.name)

    def accept(self, v: TACVisitor) -> None:
        v.visitLoadGlobalAddr(self)

class LoadFromMem(TACInstr):
    def __init__(self, dst: Temp, addr: Temp, offset : int) -> None:
        super().__init__(InstrKind.SEQ, [dst], [addr], None)
        self.dst = dst
        self.addr = addr
        self.offset = offset

    def __str__(self) -> str:
        return "%s = LOAD %s, %d" % (self.dsts[0], self.srcs[0], self.offset)

    def accept(self, v: TACVisitor) -> None:
        v.visitLoadFromMem(self)

class StoreToMem(TACInstr):
    def __init__(self, value: Temp, offset : int, addr : Temp) -> None:
        super().__init__(InstrKind.SEQ, [], [value, addr], None)
        self.addr = addr
        self.offset = offset
        self.value = value

    def __str__(self) -> str:
        # 0 for addr, 1 for value
        return "STORE %s, %d(%s)" % (self.value, self.offset, self.addr)

    def accept(self, v: TACVisitor) -> None:
        v.visitStoreToMem(self)

# step 11
class Alloc(TACInstr):
    def __init__(self, dst: Temp, size: int) -> None:
        super().__init__(InstrKind.SEQ, [dst], [], None)
        self.dst = dst
        self.size = size

    def __str__(self) -> str:
        return "%s = ALLOC %d" % (self.dsts[0], self.size)

    def accept(self, v: TACVisitor) -> None:
        v.visitAlloc(self)
