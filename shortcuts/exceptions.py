class ParsingError(RuntimeError):
    def __init__(self, msg, input, *args: object) -> None:
        super().__init__(msg, input, *args)
        self.input= input
        self.msg = msg
    pass