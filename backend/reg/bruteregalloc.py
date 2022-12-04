import random

from backend.dataflow.basicblock import BasicBlock, BlockKind
from backend.dataflow.cfg import CFG
from backend.dataflow.loc import Loc
from backend.reg.regalloc import RegAlloc
from backend.riscv.riscvasmemitter import RiscvAsmEmitter
from backend.subroutineemitter import SubroutineEmitter
from backend.subroutineinfo import SubroutineInfo
from utils.riscv import Riscv
from utils.tac.holeinstr import HoleInstr
from utils.tac.reg import Reg
from utils.tac.temp import Temp

from backend.riscv.riscvasmemitter import RiscvSubroutineEmitter

from utils.error import IllegalArgumentException

"""
BruteRegAlloc: one kind of RegAlloc

bindings: map from temp.index to Reg

we don't need to take care of GlobalTemp here
because we can remove all the GlobalTemp in selectInstr process

1. accept：根据每个函数的 CFG 进行寄存器分配，寄存器分配结束后生成相应汇编代码
2. bind：将一个 Temp 与寄存器绑定
3. unbind：将一个 Temp 与相应寄存器解绑定
4. localAlloc：根据数据流对一个 BasicBlock 内的指令进行寄存器分配
5. allocForLoc：每一条指令进行寄存器分配
6. allocRegFor：根据数据流决定为当前 Temp 分配哪一个寄存器
"""

class BruteRegAlloc(RegAlloc):
    def __init__(self, emitter: RiscvAsmEmitter) -> None:
        super().__init__(emitter)
        self.bindings = {}
        for reg in emitter.allocatableRegs:
            reg.used = False

        self.call_argument_list : list[Reg] = []

    def accept(self, graph: CFG, info: SubroutineInfo) -> None:
        # this is for a singal function
        # here graph stand for the CFG of this function

        # this is the entrance of temp allocate to reg

        # create subroutine emiter for this funtion 
        subEmitter = self.emitter.emitSubroutine(info)

        # self.bind(Temp(-1), Riscv.FP)

        for bb in graph.iterator():
            # you need to think more here
            # maybe we don't need to alloc regs for all the basic blocks

            # if this block is unreachable, then skip it
            if graph.unreachable(bb):
                continue

            if bb.label is not None:
                # emit label
                subEmitter.emitLabel(bb.label)


            # for loc in bb.locs:
            #     print(loc.instr)

            # breakpoint()

            # allocate for this basic block
            self.localAlloc(bb, subEmitter)

        subEmitter.emitEnd()

    def bind(self, temp: Temp, reg: Reg):
        reg.used = True
        self.bindings[temp.index] = reg
        reg.occupied = True
        reg.temp = temp

    def unbind(self, temp: Temp):
        if temp.index in self.bindings:
            self.bindings[temp.index].occupied = False
            self.bindings.pop(temp.index)

    def localAlloc(self, bb: BasicBlock, subEmitter: SubroutineEmitter):
        # allocate a singal basic block

        # for each basic block, clear all binds
        self.bindings.clear()
        # clear for all regs, since it is a basic block
        for reg in self.emitter.allocatableRegs:
            reg.occupied = False


        # in step9, you may need to think about how to store callersave regs here
        # loc stand for line of code
        for loc in bb.allSeq():
            # emit each line of code 
            subEmitter.emitComment(str(loc.instr)) # this is used for debug

            # allocate register for this line of code 
            self.allocForLoc(loc, subEmitter)

        # end of emit basic block
        for tempindex in bb.liveOut:
            if tempindex in self.bindings:
                subEmitter.emitStoreToStack(self.bindings.get(tempindex))

        if (not bb.isEmpty()) and (bb.kind is not BlockKind.CONTINUOUS):
            self.allocForLoc(bb.locs[len(bb.locs) - 1], subEmitter)

    def allocForLoc(self, loc: Loc, subEmitter: RiscvSubroutineEmitter):
        # emit for a line of code 
        instr = loc.instr
        srcRegs: list[Reg] = []
        dstRegs: list[Reg] = []

        # if isinstance(instr, Riscv.Param):
        #     breakpoint()

        # allocate reg for src temps
        for i in range(len(instr.srcs)):
            temp = instr.srcs[i]
            if isinstance(temp, Reg):
                srcRegs.append(temp)
            else:
                srcRegs.append(self.allocRegFor(temp, True, loc.liveIn, subEmitter))

        # allocate reg for dst temps
        for i in range(len(instr.dsts)):
            temp = instr.dsts[i]
            if isinstance(temp, Reg):
                dstRegs.append(temp)
            else:
                dstRegs.append(self.allocRegFor(temp, False, loc.liveIn, subEmitter))

        # if push, then do nothing, just store the argument and its offset
        if isinstance(instr, Riscv.Param):
            # we do not need to do toNative here
            argument_reg = srcRegs[0]
            
            # argument gere is sequence, do not need to record offset
            self.call_argument_list.append(argument_reg)

        # if call, calculate all space need
        elif isinstance(instr, Riscv.Call):
            # store calller save
            # here i sill check if it is used
            used_caller_saved = []

            for reg in self.emitter.callerSaveRegs:
                if reg.isUsed():
                    used_caller_saved.append(reg)

            # caller save reg name, correspond to its offset accrod to SP
            caller_save_dict = {}

            # store to stack
            for reg in used_caller_saved:
                subEmitter.emitStoreToStack(reg)
                caller_save_dict[reg.name] = subEmitter.offsets[reg.temp.index]

            # have to do it by human
            argument_len = len(self.call_argument_list)

            if argument_len <= 8:
                for i in range(argument_len):
                    # self.call_argument_list = list[Reg]
                    reg_name = self.call_argument_list[i].name
                    if reg_name in caller_save_dict:
                        # if this register is stored on stack
                        subEmitter.emitNative(Riscv.NativeLoadWord(Riscv.ArgRegs[i], Riscv.SP, caller_save_dict[reg_name]))
                    else:
                        # just do move is ok
                        subEmitter.emitNative(Riscv.NativeMove(Riscv.ArgRegs[i], self.call_argument_list[i]))
                
            else:
                
                # do this first
                # others on stack
                others_num = argument_len - 8
                subEmitter.emitNative(Riscv.SPAdd(- others_num * 4))

                for i in range(8, argument_len):
                    argument_reg = self.call_argument_list[i]
                    subEmitter.emitNative(
                        Riscv.NativeStoreWord(argument_reg, Riscv.SP, (i - 8) * 4)
                    )

                # pass the first 8 from registers
                for i in range(8):
                    # self.call_argument_list = list[Reg]
                    argument_reg = self.call_argument_list[i]
                    reg_name = argument_reg.name

                    if reg_name in caller_save_dict:
                        # if this register is stored on stack
                        subEmitter.emitNative(Riscv.NativeLoadWord(Riscv.ArgRegs[i], Riscv.SP, caller_save_dict[reg_name] + others_num * 4))
                    else:
                        # just do move is ok
                        subEmitter.emitNative(Riscv.NativeMove(Riscv.ArgRegs[i], argument_reg))

            # clear call_argument_list
            self.call_argument_list = []

            # call function, i.e. toNative
            subEmitter.emitNative(instr.toNative(dstRegs, srcRegs))

            # move result to target reg has been done by Get_Function_Result instruction

            # restore argument stack
            # only when argument num over than 8
            if argument_len > 8:
                subEmitter.emitNative(Riscv.SPAdd((argument_len - 8) * 4))

            # # restore caller saved register
            for reg in used_caller_saved:
                subEmitter.emitLoadFromStack(reg, reg.temp)

        
        elif isinstance(instr, Riscv.Get_Function_Result):
            subEmitter.emitNative(Riscv.NativeMove(dstRegs[0], Riscv.A0))

        else:
            # other instructions
            # change TAC instruction to Native instruction
            subEmitter.emitNative(instr.toNative(dstRegs, srcRegs))


    def allocRegFor(
        self, temp: Temp, isRead: bool, live: set[int], subEmitter: SubroutineEmitter
    ):
        if temp.index in self.bindings:
            return self.bindings[temp.index]

        for reg in self.emitter.allocatableRegs:
            if (not reg.occupied) or (not reg.temp.index in live):
                subEmitter.emitComment(
                    "  allocate {} to {}  (read: {}):".format(
                        str(temp), str(reg), str(isRead)
                    )
                )
                if isRead:
                    subEmitter.emitLoadFromStack(reg, temp)
                if reg.occupied:
                    self.unbind(reg.temp)
                self.bind(temp, reg)
                return reg

        reg = self.emitter.allocatableRegs[
            random.randint(0, len(self.emitter.allocatableRegs))
        ]
        subEmitter.emitStoreToStack(reg)
        subEmitter.emitComment("  spill {} ({})".format(str(reg), str(reg.temp)))
        self.unbind(reg.temp)
        self.bind(temp, reg)
        subEmitter.emitComment(
            "  allocate {} to {} (read: {})".format(str(temp), str(reg), str(isRead))
        )
        if isRead:
            subEmitter.emitLoadFromStack(reg, temp)
        return reg
