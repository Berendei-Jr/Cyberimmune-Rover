import logging

from core.action import Action


class Connector:
    def __init__(self, name: str) -> None:
        self.name = name
        self.logger = logging.getLogger(name)

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def get_info(self) -> dict:
        pass

    def perform_actions(self, actions: list[Action]) -> None:
        pass
