from core.action import Action


class StopAction(Action):
    def __init__(self, description="Выключение двигателя"):
        super().__init__(name=type(self).__name__, description=description)
