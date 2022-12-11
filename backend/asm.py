from backend.dataflow.cfg import CFG
from backend.dataflow.cfgbuilder import CFGBuilder
from backend.dataflow.livenessanalyzer import LivenessAnalyzer
from backend.reg.bruteregalloc import BruteRegAlloc
from backend.riscv.riscvasmemitter import RiscvAsmEmitter
from utils.tac.tacprog import TACProg

"""
Asm: we use it to generate all the asm code for the program
"""

class Asm:
    def __init__(self, emitter: RiscvAsmEmitter, regAlloc: BruteRegAlloc) -> None:
        self.emitter = emitter
        self.regAlloc = regAlloc

    def transform(self, prog: TACProg):

        # the entrance of riscv stage

        analyzer = LivenessAnalyzer()

        for func in prog.funcs:
            # pair[0] is instructions, pair[1] is function label

            # translate TAC instr to riscv instr
            # therefore we should deal with callee save and put parameter to stack here
            pair = self.emitter.selectInstr(func) 

            # pair[0] = list[Riscv.Instr]
            # pair[1] = function info

            # for item in pair[0]:
            #     print(item)
            # print("-" * 50)


            builder = CFGBuilder()
            cfg: CFG = builder.buildFrom(pair[0])
            analyzer.accept(cfg)

            # allocate regs for tac virtual reg
            self.regAlloc.accept(cfg, pair[1])

            # for item in pair[0]:
            #     print(item)
            # print()

            # # print("-" * 50)


        ret = self.emitter.emitEnd()

        # print(ret)

        # exit(0)

        return ret
