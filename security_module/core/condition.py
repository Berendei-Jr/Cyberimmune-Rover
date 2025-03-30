from typing import Any


class Condition(dict):
    def __init__(
        self,
        name: str,
        value: Any,
        description: str = "",
    ) -> None:
        dict.__init__(self, name=name, value=value, description=description)
