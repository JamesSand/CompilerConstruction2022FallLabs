from typing import Final, Optional

from utils.label.funclabel import FuncLabel
from utils.label.label import Label, LabelKind
from utils.tac.holeinstr import HoleInstr
from utils.tac.nativeinstr import NativeInstr
from utils.tac.reg import Reg
from utils.tac.tacinstr import TACInstr
from utils.tac.tacop import BinaryOp, InstrKind, UnaryOp
from utils.tac.temp import Temp

WORD_SIZE: Final[int] = 4  # in bytes
MAX_INT: Final[int] = 0x7FFF_FFFF


class Riscv:

    ZERO = Reg(0, "x0")  # always zero
    RA = Reg(1, "ra")  # return address
    SP = Reg(2, "sp")  # stack pointer
    GP = Reg(3, "gp")  # global pointer
    TP = Reg(4, "tp")  # thread pointer
    T0 = Reg(5, "t0")
    T1 = Reg(6, "t1")
    T2 = Reg(7, "t2")
    FP = Reg(8, "fp")  # frame pointer
    S1 = Reg(9, "s1")
    A0 = Reg(10, "a0")
    A1 = Reg(11, "a1")
    A2 = Reg(12, "a2")
    A3 = Reg(13, "a3")
    A4 = Reg(14, "a4")
    A5 = Reg(15, "a5")
    A6 = Reg(16, "a6")
    A7 = Reg(17, "a7")
    S2 = Reg(18, "s2")
    S3 = Reg(19, "s3")
    S4 = Reg(20, "s4")
    S5 = Reg(21, "s5")
    S6 = Reg(22, "s6")
    S7 = Reg(23, "s7")
    S8 = Reg(24, "s8")
    S9 = Reg(25, "s9")
    S10 = Reg(26, "s10")
    S11 = Reg(27, "s11")
    T3 = Reg(28, "t3")
    T4 = Reg(29, "t4")
    T5 = Reg(30, "t5")
    T6 = Reg(31, "t6")

    CallerSaved = [T0, T1, T2, T3, T4, T5, T6, A1, A2, A3, A4, A5, A6, A7]

    CalleeSaved = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11]

    AllocatableRegs = CallerSaved + CalleeSaved

    ArgRegs = [A0, A1, A2, A3, A4, A5, A6, A7]

    EPILOGUE_SUFFIX = "_exit"

    FMT1 = "{}"
    FMT2 = "{}, {}"
    FMT3 = "{}, {}, {}"
    FMT_OFFSET = "{}, {}({})"
    # Todo FMT4

    class JumpToEpilogue(TACInstr):
        def __init__(self, label: Label) -> None:
            super().__init__(
                InstrKind.RET,
                [],
                [],
                Label(LabelKind.TEMP, label.name + Riscv.EPILOGUE_SUFFIX),
            )

        def __str__(self) -> str:
            return "j " + str(self.label)

    class RiscvLabel(TACInstr):
        def __init__(self, label: Label) -> None:
            super().__init__(InstrKind.LABEL, [], [], label)

        def __str__(self) -> str:
            return str(self.label) + ":"

        def isLabel(self) -> bool:
            return True

    class LoadImm(TACInstr):
        def __init__(self, dst: Temp, value: int) -> None:
            super().__init__(InstrKind.SEQ, [dst], [], None)
            self.value = value

        def __str__(self) -> str:
            return "li " + Riscv.FMT2.format(str(self.dsts[0]), self.value)

    class Move(TACInstr):
        def __init__(self, dst: Temp, src: Temp) -> None:
            super().__init__(InstrKind.SEQ, [dst], [src], None)

        def __str__(self) -> str:
            return "mv " + Riscv.FMT2.format(str(self.dsts[0]), str(self.srcs[0]))

    class NativeMove(NativeInstr):
        def __init__(self, dst: Reg, src: Reg) -> None:
            super().__init__(InstrKind.SEQ, [dst], [src], None)

        def __str__(self) -> str:
            return "mv " + Riscv.FMT2.format(str(self.dsts[0]), str(self.srcs[0]))

    class Unary(TACInstr):
        def __init__(self, op: UnaryOp, dst: Temp, src: Temp) -> None:
            super().__init__(InstrKind.SEQ, [dst], [src], None)
            self.op = op.__str__()[8:].lower()

        def __str__(self) -> str:
            return "{} ".format(self.op) + Riscv.FMT2.format(
                str(self.dsts[0]), str(self.srcs[0])
            )

    class Binary(TACInstr):
        def __init__(self, op: BinaryOp, dst: Temp, src0: Temp, src1: Temp) -> None:
            super().__init__(InstrKind.SEQ, [dst], [src0, src1], None)
            self.op = op.__str__()[9:].lower()

        def __str__(self) -> str:
            return "{} ".format(self.op) + Riscv.FMT3.format(
                str(self.dsts[0]), str(self.srcs[0]), str(self.srcs[1])
            )
    
    class Branch(TACInstr):
        def __init__(self, cond: Temp, target: Label) -> None:
            super().__init__(InstrKind.COND_JMP, [], [cond], target)
            self.target = target
        
        def __str__(self) -> str:
            return "beq " + Riscv.FMT3.format(str(Riscv.ZERO), str(self.srcs[0]), str(self.target))

    class Jump(TACInstr):
        def __init__(self, target: Label) -> None:
            super().__init__(InstrKind.JMP, [], [], target)
            self.target = target
        
        def __str__(self) -> str:
            return "j " + str(self.target)

    class SPAdd(NativeInstr):
        def __init__(self, offset: int) -> None:
            super().__init__(InstrKind.SEQ, [Riscv.SP], [Riscv.SP], None)
            self.offset = offset

        def __str__(self) -> str:
            assert -2048 <= self.offset <= 2047  # Riscv imm [11:0]
            return "addi " + Riscv.FMT3.format(
                str(Riscv.SP), str(Riscv.SP), str(self.offset)
            )

    class Set_FP_accrod_SP(NativeInstr):
        def __init__(self, offset : int) -> None:
            super().__init__(InstrKind.SEQ, [Riscv.FP], [Riscv.SP], None)
            self.offset = offset

        def __str__(self) -> str:
            return "addi " + Riscv.FMT3.format(
                str(Riscv.FP), str(Riscv.SP), str(self.offset)
            )

    class NativeStoreWord(NativeInstr):
        def __init__(self, src: Reg, base: Reg, offset: int) -> None:
            super().__init__(InstrKind.SEQ, [], [src, base], None)
            self.offset = offset

        def __str__(self) -> str:
            assert -2048 <= self.offset <= 2047  # Riscv imm [11:0]
            return "sw " + Riscv.FMT_OFFSET.format(
                str(self.srcs[0]), str(self.offset), str(self.srcs[1])
            )

    class NativeLoadWord(NativeInstr):
        def __init__(self, dst: Reg, base: Reg, offset: int) -> None:
            super().__init__(InstrKind.SEQ, [dst], [base], None)
            self.offset = offset

        def __str__(self) -> str:
            assert -2048 <= self.offset <= 2047  # Riscv imm [11:0]
            return "lw " + Riscv.FMT_OFFSET.format(
                str(self.dsts[0]), str(self.offset), str(self.srcs[0])
            )

    class NativeReturn(NativeInstr):
        def __init__(self) -> None:
            super().__init__(InstrKind.RET, [Riscv.RA], [], None)

        def __str__(self) -> str:
            return "ret"

    class Push(TACInstr):
        def __init__(self, temp_to_store : Temp, offset : int) -> None:
            super().__init__(InstrKind.SEQ, [], [temp_to_store], None)
            self.temp_to_store = temp_to_store
            self.offset = offset
        
        def __str__(self) -> str:
            return "sw " + Riscv.FMT_OFFSET.format(
                str(self.temp_to_store), str(self.offset), str(Riscv.SP)
            )

    class Call(TACInstr):
        def __init__(self, target: Label) -> None:
            super().__init__(InstrKind.SEQ, [Riscv.A0, Riscv.RA], [], target)
            self.target = target
        
        def __str__(self) -> str:
            return "call " + str(self.target)

    class Get_Function_Result(TACInstr):
        def __init__(self, funct_result_temp : Temp) -> None:
            super().__init__(InstrKind.SEQ, [funct_result_temp], [Riscv.A0], None)
            self.funct_result_temp = funct_result_temp
        
        def __str__(self) -> str:
            return "mv " + Riscv.FMT2.format(
                str(self.funct_result_temp), 
                # function result store in a0
                str(Riscv.A0)
            )

    class Param(TACInstr):
        def __init__(self, index : int, param_temp : Temp) -> None:
            super().__init__(InstrKind.SEQ, [], [param_temp], None)
            self.param_temp = param_temp
            self.index = index
        
        def __str__(self) -> str:
            return "param " + Riscv.FMT2.format(
                str(self.index),
                str(self.param_temp)
            )

    # step 10 codes here
    class LoadGlobalAddr(TACInstr):
        def __init__(self, dst: Temp, name: str) -> None:
            super().__init__(InstrKind.SEQ, [dst], [], None)
            self.name = name

        def __str__(self) -> str:
            return "la " + Riscv.FMT2.format(str(self.dsts[0]), self.name)

    class LoadFromMem(TACInstr):
        def __init__(self, dst: Temp, offset: int, addr: Temp) -> None:
            super().__init__(InstrKind.SEQ, [dst], [addr], None)
            self.offset = offset

        def __str__(self) -> str:
            return "lw " + Riscv.FMT_OFFSET.format(self.dsts[0], self.offset, self.srcs[0])

    class StoreToMem(TACInstr):
        def __init__(self, value: Temp, offset: int, addr : Temp) -> None:
            super().__init__(InstrKind.SEQ, [], [value, addr], None)
            self.offset = offset

        def __str__(self) -> str:
            return "sw " + Riscv.FMT_OFFSET.format(self.srcs[0], self.offset, self.srcs[1])