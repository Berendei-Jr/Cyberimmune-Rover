from core.condition import Condition


class GroundSpeed(Condition):
    def __init__(self, value: float, description: str = "Ограничение скорости") -> None:
        super().__init__(type(self).__name__, value, description)

    def perform_check(self, current_state: dict) -> bool:
        return current_state["groundspeed"] > self["value"]
