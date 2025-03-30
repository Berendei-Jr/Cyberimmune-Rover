import logging

from connectors.sitl.sitl_connector import (
    SitlConnector,
)
from core.file_manager import FileManager
from core.log_formater import pretty_list


class SecurityModule:
    def __init__(
        self,
        connector: str = "SITL",
        **kwargs,
    ):
        self.logger = logging.getLogger(type(self).__name__)

        if connector == "SITL":
            self.connector = SitlConnector(sv_manager=kwargs["sv_manager"])
        else:
            raise NotImplementedError(f"Connector {connector} not implemented")

        self.file_manager = FileManager(
            route_file_path=kwargs["route_file_path"],
            security_file_path=kwargs["security_file_path"],
        )
        self.policies = self.file_manager.read_security_file()

        self.logger.info(
            "Security module initialized. Loaded policies:" + pretty_list([policy["name"] for policy in self.policies])
        )

    def run(self):
        self.connector.connect()
        while True:
            current_state = self.connector.get_info()
            for policy in self.policies:
                if not policy.perform_check(current_state):
                    self.connector.perform_actions(policy.get_actions())
        self.connector.disconnect()
