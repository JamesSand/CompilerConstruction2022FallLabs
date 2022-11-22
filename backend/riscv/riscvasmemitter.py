from typing import Sequence, Tuple

from backend.asmemitter import AsmEmitter
from utils.error import IllegalArgumentException
from utils.label.label import Label, LabelKind
from utils.riscv import Riscv
from utils.tac.reg import Reg
from utils.tac.tacfunc import TACFunc
from utils.tac.tacinstr import *
from utils.tac.tacvisitor import TACVisitor

from ..subroutineemitter import SubroutineEmitter
from ..subroutineinfo import SubroutineInfo

"""
RiscvAsmEmitter: an AsmEmitter for RiscV
"""


class RiscvAsmEmitter(AsmEmitter):
    def __init__(
        self,
        allocatableRegs: list[Reg],
        callerSaveRegs: list[Reg],
    ) -> None:
        super().__init__(allocatableRegs, callerSaveRegs)

    
        # the start of the asm code
        # int step10, you need to add the declaration of global var here
        self.printer.println(".text")
        self.printer.println(".global main")
        self.printer.println("")

    # transform tac instrs to RiscV instrs
    # collect some info which is saved in SubroutineInfo for SubroutineEmitter
    def selectInstr(self, func: TACFunc) -> tuple[list[str], SubroutineInfo]:

        selector: RiscvAsmEmitter.RiscvInstrSelector = (
            RiscvAsmEmitter.RiscvInstrSelector(func.entry)
        )
        for instr in func.getInstrSeq():
            # breakpoint()
            # here instr is a derive class of tacinstr
            # tacintr is only an abstracat and basic class

            # each line of word accept themselves
            # the visitor is RiscvInstrSelector
            instr.accept(selector)

        info = SubroutineInfo(func.entry)
        # breakpoint()

        return (selector.seq, info)

    # use info to construct a RiscvSubroutineEmitter
    def emitSubroutine(self, info: SubroutineInfo):
        return RiscvSubroutineEmitter(self, info)

    # return all the string stored in asmcodeprinter
    def emitEnd(self):
        return self.printer.close()

    class RiscvInstrSelector(TACVisitor):
        def __init__(self, entry: Label) -> None:
            self.entry = entry
            self.seq = []

            self.parameter_to_push = []

        # in step11, you need to think about how to deal with globalTemp in almost all the visit functions. 
        def visitReturn(self, instr: Return) -> None:
            if instr.value is not None:
                self.seq.append(Riscv.Move(Riscv.A0, instr.value))
            else:
                self.seq.append(Riscv.LoadImm(Riscv.A0, 0))
            self.seq.append(Riscv.JumpToEpilogue(self.entry))

        def visitMark(self, instr: Mark) -> None:
            self.seq.append(Riscv.RiscvLabel(instr.label))

        def visitLoadImm4(self, instr: LoadImm4) -> None:
            self.seq.append(Riscv.LoadImm(instr.dst, instr.value))

        def visitUnary(self, instr: Unary) -> None:
            self.seq.append(Riscv.Unary(instr.op, instr.dst, instr.operand))
 
        def visitBinary(self, instr: Binary) -> None:
            # node.BinaryOp.EQ : tacop.BinaryOp.EQU,
            # node.BinaryOp.NE : tacop.BinaryOp.NEQ,
            # node.BinaryOp.LE : tacop.BinaryOp.LEQ,
            # node.BinaryOp.GE : tacop.BinaryOp.GEQ,
            # node.BinaryOp.LogicAnd :tacop.BinaryOp.LAND,
            # node.BinaryOp.LogicOr : tacop.BinaryOp.LOR,
            
            if instr.op == BinaryOp.EQU:
                self.seq.append(Riscv.Binary(BinaryOp.SUB, instr.dst, instr.lhs, instr.rhs))
                self.seq.append(Riscv.Unary(UnaryOp.SEQZ, instr.dst, instr.dst))
            elif instr.op == BinaryOp.NEQ:
                self.seq.append(Riscv.Binary(BinaryOp.SUB, instr.dst, instr.lhs, instr.rhs))
                self.seq.append(Riscv.Unary(UnaryOp.SNEZ, instr.dst, instr.dst))
            elif instr.op == BinaryOp.LEQ:
                # sgt	a0,a0,a1
	            # xori	a0,a0,1
                self.seq.append(Riscv.Binary(BinaryOp.SGT, instr.dst, instr.lhs, instr.rhs))
                self.seq.append(Riscv.Unary(UnaryOp.SEQZ, instr.dst,instr.dst ))
            elif instr.op == BinaryOp.GEQ:
                # slt	a0,a0,a1
	            # xori	a0,a0,1
                self.seq.append(Riscv.Binary(BinaryOp.SLT, instr.dst, instr.lhs, instr.rhs))
                self.seq.append(Riscv.Unary(UnaryOp.SEQZ, instr.dst,instr.dst ))
            elif instr.op == BinaryOp.AND:
                self.seq.append(Riscv.Unary(UnaryOp.SNEZ, instr.dst,instr.lhs ))
                # 这里缺了一个伪指令
                self.seq.append(Riscv.Binary(BinaryOp.AND, instr.dst, instr.dst, instr.rhs))
                self.seq.append(Riscv.Unary(UnaryOp.SNEZ, instr.dst,instr.dst ))
                
            elif instr.op == BinaryOp.OR:
                self.seq.append(Riscv.Binary(BinaryOp.OR, instr.dst, instr.lhs, instr.rhs))
                self.seq.append(Riscv.Unary(UnaryOp.SNEZ, instr.dst, instr.dst))
            
            else:
                self.seq.append(Riscv.Binary(instr.op, instr.dst, instr.lhs, instr.rhs))

        def visitCondBranch(self, instr: CondBranch) -> None:
            self.seq.append(Riscv.Branch(instr.cond, instr.label))
        
        def visitBranch(self, instr: Branch) -> None:
            self.seq.append(Riscv.Jump(instr.target))

        def visitAssign(self, instr: Assign) -> None:
            self.seq.append(Riscv.Move(instr.dst, instr.src))

        # in step9, you need to think about how to pass the parameters and how to store and restore callerSave regs
        
        def visitParameter(self, instr : Param):
            # we will push all parameter to the stack when we collect all of them
            parameter_temp = instr.parameter
            self.parameter_to_push.append(parameter_temp)

        def visitCall(self, call : Call):
            # we only need to consider parameter passing and function calling here

            param_num = len(self.parameter_to_push)

            # we donot need to do very specific things here
            for i in range(param_num):
                self.seq.append(Riscv.Param(i, self.parameter_to_push[i]))
            
            # clear argument temp list
            self.parameter_to_push = []

            # call the function
            funct_label = call.target
            self.seq.append(Riscv.Call(funct_label))

            # self.seq.append()            

            # restore result to target register
            # since here src is Reg and dst is Temp, so we need a new Risc class
            function_result_temp = call.result
            self.seq.append(Riscv.Get_Function_Result(function_result_temp))

            # I think should restore caller saved registers here

        # in step11, you need to think about how to store the array 
"""
RiscvAsmEmitter: an SubroutineEmitter for RiscV
"""

class RiscvSubroutineEmitter(SubroutineEmitter):
    def __init__(self, emitter: RiscvAsmEmitter, info: SubroutineInfo) -> None:
        super().__init__(emitter, info)
        
        # + 4 is for the RA reg , + 4 for FP
        self.nextLocalOffset = 4 * len(Riscv.CalleeSaved) + 4 + 4
        
        # the buf which stored all the NativeInstrs in this function
        self.buf: list[NativeInstr] = []

        # from temp to int
        # record where a temp is stored in the stack
        self.offsets = {}

        self.printer.printLabel(info.funcLabel)

        # in step9, step11 you can compute the offset of local array and parameters here
        # function parameter num stored in info
        self.funct_parameter_num = info.funcLabel.parameter_num

        # on stack parameter offet relative to FP
        self.argument_offset = []
        for i in range(self.funct_parameter_num):
            self.argument_offset.append(i * 4)


    def emitComment(self, comment: str) -> None:
        # you can add some log here to help you debug
        pass
    
    # store some temp to stack
    # usually happen when reaching the end of a basicblock
    # in step9, you need to think about the fuction parameters here
    def emitStoreToStack(self, src: Reg) -> None:

        # if str(src) == "t0":
        #     breakpoint()

        if src.temp.index not in self.offsets:
            self.offsets[src.temp.index] = self.nextLocalOffset
            self.nextLocalOffset += 4

        self.buf.append(
            Riscv.NativeStoreWord(src, Riscv.SP, self.offsets[src.temp.index])
        )

        # print(Riscv.NativeStoreWord(src, Riscv.SP, self.offsets[src.temp.index]))

    # load some temp from stack
    # usually happen when using a temp which is stored to stack before
    # in step9, you need to think about the fuction parameters here
    def emitLoadFromStack(self, dst: Reg, src: Temp):

        # since function parameter always be the first virtual register
        if src.index < self.funct_parameter_num:
            # base on FP
            self.buf.append(
                Riscv.NativeLoadWord(dst, Riscv.FP, self.argument_offset[src.index])
            )

            return

        if src.index not in self.offsets:
            breakpoint()
            raise IllegalArgumentException()
        else:
            self.buf.append(
                Riscv.NativeLoadWord(dst, Riscv.SP, self.offsets[src.index])
            )

    # add a NativeInstr to buf
    # when calling the fuction emitEnd, all the instr in buf will be transformed to RiscV code
    def emitNative(self, instr: NativeInstr):
        self.buf.append(instr)

    def emitLabel(self, label: Label):
        self.buf.append(Riscv.RiscvLabel(label).toNative([], []))

    
    def emitEnd(self):
        # before the real function
        # store callee saved registers
        self.printer.printComment("start of prologue")

        # we first sub the stack here
        # therefore we can save by adding to SP later

        self.printer.printInstr(Riscv.SPAdd(-self.nextLocalOffset))

        # in step9, you need to think about how to store RA here
        # you can get some ideas from how to save CalleeSaved regs
        for i in range(len(Riscv.CalleeSaved)):
            if Riscv.CalleeSaved[i].isUsed():
                self.printer.printInstr(
                    Riscv.NativeStoreWord(Riscv.CalleeSaved[i], Riscv.SP, 4 * i)
                )

        # also store ra here
        self.printer.printInstr(
            Riscv.NativeStoreWord(Riscv.RA, Riscv.SP, 4 * len(Riscv.CalleeSaved))
        )

        self.printer.printInstr(
            Riscv.NativeStoreWord(Riscv.FP, Riscv.SP, 4 * len(Riscv.CalleeSaved) + 4)
        )

        # done all callee save

        # remember current next local offset
        self.prologue_next_local_offset = self.nextLocalOffset 

        # set FP relative to SP
        self.printer.printInstr(
            Riscv.Set_FP_accrod_SP(self.nextLocalOffset)
        )

        self.printer.printComment("end of prologue")
        self.printer.println("")

        self.printer.printComment("start of body")

        # in step9, you need to think about how to pass the parameters here
        # you can use the stack or regs


        # using asmcodeprinter to output the RiscV code
        for instr in self.buf:
            self.printer.printInstr(instr)

        self.printer.printComment("end of body")
        self.printer.println("")

        self.printer.printLabel(
            Label(LabelKind.TEMP, self.info.funcLabel.name + Riscv.EPILOGUE_SUFFIX)
        )
        self.printer.printComment("start of epilogue")

        # print("before callee save restore")
        for i in range(len(Riscv.CalleeSaved)):
            if Riscv.CalleeSaved[i].isUsed():
                # print("restore")
                self.printer.printInstr(
                    Riscv.NativeLoadWord(Riscv.CalleeSaved[i], Riscv.SP, 4 * i)
                )

        # restore ra
        self.printer.printInstr(
            Riscv.NativeLoadWord(Riscv.RA, Riscv.SP, 4 * len(Riscv.CalleeSaved))
        )

        self.printer.printInstr(
            Riscv.NativeLoadWord(Riscv.FP, Riscv.SP, 4 * len(Riscv.CalleeSaved) + 4)
        )

        self.printer.printInstr(Riscv.SPAdd(self.nextLocalOffset))
        self.printer.printComment("end of epilogue")
        self.printer.println("")

        self.printer.printInstr(Riscv.NativeReturn())
        self.printer.println("")
