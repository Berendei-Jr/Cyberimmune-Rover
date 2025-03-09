from connectors.sitl.sitl_connector import SitlConnector
from core.policies import Condition, SpeedRestriction


class SecurityModule:
    def __init__(self, connector: str = "SITL", policies: list = [SpeedRestriction([Condition("Speed", "", 3)])]):
        if connector == "SITL":
            self.connector = SitlConnector()
        else:
            raise NotImplementedError(f"Connector {connector} not implemented")
        self.policies = policies

    def run(self):
        self.connector.connect()
        while True:
            current_state = self.connector.get_info()
            for policy in self.policies:
                if not policy.perform_check(current_state):
                    self.connector.perform_action(policy.get_action())
        self.connector.disconnect()
