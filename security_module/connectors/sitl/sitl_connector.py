import time
from pathlib import Path

import pexpect
from connectors.connector import Connector
from connectors.sitl.sim_vehicle_manager import (
    SimVehicleManager,
    execute_mavproxy_command,
)
from core.action import Action
from core.log_formater import colored_text
from parameters.actions import *
from parameters.conditions import *

ARDUPILOT_DIR = Path(__file__).parent.parent.parent.parent
MAVPROXY_COMMAND = "python3 venv/bin/mavproxy.py --sitl 127.0.0.1:5501"


class SitlConnector(Connector):
    def __init__(
        self,
        name: str = "Sitl connector",
        sv_manager: SimVehicleManager = None,
    ):
        super().__init__(name)
        self.sv_manager = sv_manager
        if self.sv_manager:
            self.logger.info("Sim vehicle manager provided")

    def __del__(self):
        self.disconnect()

    def connect(self):
        self.logger.info("Trying to connect to Ardupilot...")
        self.process = pexpect.spawn(MAVPROXY_COMMAND, cwd=ARDUPILOT_DIR)
        try:
            self.process.expect("Detected vehicle", timeout=5)
        except pexpect.exceptions.TIMEOUT as e:
            raise RuntimeError(
                "Unable to connect to Ardupilot. SITL and Mavproxy must be running before starting security module"
            ) from e
        self.logger.info(
            colored_text(
                "Connection to Ardupilot established",
                "green",
            )
        )

    def disconnect(self):
        if hasattr(self, "process"):
            self.process.close()
            self.logger.warning(colored_text("Ardupilot stopped", "red"))

    def get_info(self):
        execute_mavproxy_command(self.process, "status", "VIBRATION")
        for line in self.process.before.decode().splitlines():
            if "VFR_HUD" in line:
                data_str = line.split("{", 1)[1].rsplit("}", 1)[0]
                data_dict = {}
                for item in data_str.split(","):
                    key, value = item.split(":", 1)
                    data_dict[key.strip()] = float(value.strip()) if "." in value else int(value.strip())
                return data_dict

    def perform_actions(self, actions: list[Action]):
        for action in actions:
            self.logger.info("Performing action %s...", action["name"])
            if type(action) == StopAction:
                self._stop_action()
            else:
                raise NotImplementedError(f"Action {action['name']} not implemented")

    def _stop_action(self):
        if self.sv_manager:
            rc = self.sv_manager.send_mavproxy_command(
                command="disarm",
                expected_response="DISARMED",
                timeout=3,
            )
            if rc:
                raise RuntimeError("Unable to disarm throttle")
            self.logger.info(colored_text("Throttle disarmed", "yellow"))
            time.sleep(1)
