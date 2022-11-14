from .label import Label, LabelKind


class FuncLabel(Label):
    def __init__(self, name: str, parameter_num : int = 0) -> None:
        super().__init__(LabelKind.FUNC, name)
        self.func = name
        self.parameter_num = parameter_num

    def __str__(self) -> str:
        # return "FUNCTION<%s>" % self.func
        return self.func


MAIN_LABEL = FuncLabel("main")
