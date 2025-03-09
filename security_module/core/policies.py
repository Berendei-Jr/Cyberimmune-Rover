import logging

from core.actions import StopAction


class Condition:
    def __init__(self, name: str, description: str, value) -> None:
        self.name = name
        self.description = description
        self.value = value


class Policy:
    def __init__(self, name: str, description: str, conditions: list, actions: list) -> None:
        self.name = name
        self.logger = logging.getLogger(name)
        self.description = description
        self.conditions = conditions
        self.actions = actions

    def perform_check(self, *args, **kwargs) -> bool:
        return False

    def get_action(self) -> None:
        pass

    def __str__(self) -> str:
        return self.name


class SpeedRestriction(Policy):
    def __init__(
        self, conditions: list, actions: list = [StopAction()], name: str = "Speed Restriction", description: str = ""
    ) -> None:
        assert len(conditions) == 1
        assert conditions[0].value > 0

        assert len(actions) == 1
        super().__init__(name, description, conditions, actions)

    def perform_check(self, current_state: dict) -> bool:
        check_succeded = current_state["groundspeed"] < self.conditions[0].value
        if not check_succeded:
            self.logger.info(f"Speed Restriction check found violation!")
        return check_succeded

    def get_action(self) -> None:
        return self.actions[0]
