import json
import logging

from core.action import Action
from core.condition import Condition
from core.log_formater import colored_text, pretty_list


class Policy(dict):
    def __init__(
        self,
        name: str,
        description: str,
        conditions: list[Condition],
        actions: list[Action],
    ) -> None:
        self.logger = logging.getLogger(name)
        dict.__init__(self, name=name, description=description, conditions=conditions, actions=actions)
        self.logger.debug("%s policy initialized: %s", name, self)

    def perform_check(self, current_state: dict) -> bool:
        check_succeded = True

        for condition in self["conditions"]:
            res = condition.perform_check(current_state)
            if res:
                check_succeded = False
                self.logger.error(
                    colored_text(
                        f"{self['name']} check found violation in condition {condition['name']}!",
                        "red",
                    )
                )
        return check_succeded

    def get_actions(self) -> list[Action]:
        return self["actions"]

    def __str__(self) -> str:
        return pretty_list([self["name"], self["description"], self["conditions"], self["actions"]])
