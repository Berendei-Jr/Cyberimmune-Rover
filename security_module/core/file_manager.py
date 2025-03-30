import json
import logging
from pathlib import Path

from core.policy import Policy
from core.log_formater import pretty_list
from parameters.actions import *
from parameters.conditions import *

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s]: %(message)s",
    datefmt="%H:%M:%S",
)


class FileManager:
    def __init__(self, route_file_path: str, security_file_path: str, name: str = "file_manager"):
        self.logger = logging.getLogger(name)

        self.route_file_path = Path(route_file_path)
        self.security_file_path = Path(security_file_path)

        if not self.route_file_path.exists():
            raise FileNotFoundError(f"Route file {self.route_file_path} does not exist")

        if not self.security_file_path.exists():
            raise FileNotFoundError(f"Security file {self.security_file_path} does not exist")

        self.logger.info(
            "File manager initialized with files:" + pretty_list([self.route_file_path, self.security_file_path])
        )

    def write_security_file(self, policies: list):
        with open(self.security_file_path, "w", encoding="utf-8") as f:
            json.dump(policies, f, indent=4, ensure_ascii=False)

        self.logger.info("Security file saved to %s", self.security_file_path)

    def read_security_file(self) -> list[Policy]:
        policies = []
        with open(self.security_file_path, "r") as f:
            policies_raw = json.load(f)

        for p in policies_raw:
            conditions = []
            conditions_raw = p["conditions"]
            for c in conditions_raw:
                c_class_name = c["name"]
                c_value = c["value"]
                c_description = c["description"]
                conditions.append(globals()[c_class_name](c_value, c_description))

            actions = []
            actions_raw = p["actions"]
            for a in actions_raw:
                a_class_name = a["name"]
                a_description = a["description"]
                actions.append(globals()[a_class_name](a_description))

            policies.append(
                Policy(
                    name=p["name"],
                    description=p["description"],
                    conditions=conditions,
                    actions=actions,
                )
            )

        return policies
