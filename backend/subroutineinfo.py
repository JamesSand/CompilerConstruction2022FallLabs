from utils.label.funclabel import FuncLabel

"""
SubroutineInfo: collect some info when selecting instr which will be used in SubroutineEmitter
"""


class SubroutineInfo:
    def __init__(self, funcLabel: FuncLabel, array_size : int) -> None:
        self.funcLabel = funcLabel
        self.array_size = array_size

    def __str__(self) -> str:
        return "funcLabel: {}".format(
            self.funcLabel.name,
        )
