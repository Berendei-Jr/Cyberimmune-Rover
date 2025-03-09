class Action:
    def __init__(self, name):
        self.name = name


class StopAction(Action):
    def __init__(self, name="Stop Action"):
        super().__init__(name)
