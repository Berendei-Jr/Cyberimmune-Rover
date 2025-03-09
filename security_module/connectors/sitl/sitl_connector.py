import logging
from pathlib import Path

import pexpect
from connectors.connector import *
from core.actions import *

ARDUPILOT_DIR = Path(__file__).parent.parent.parent.parent
MAVPROXY_COMMAND = "python3 venv/bin/mavproxy.py --sitl 127.0.0.1:5501"


def run_command(process, command, expected, retry=0):
    try:
        process.sendline(command)
        process.expect(expected, timeout=3)
    except pexpect.exceptions.TIMEOUT as e:
        retry += 1
        if retry < 2:
            logging.error(f"Command '{command}' timed out. Repeating...")
            run_command(process, command, expected, retry)
        else:
            raise RuntimeError(f"Command '{command}' timed out. Giving up.") from e


class SitlConnector(Connector):
    def __init__(self, name: str = "Sitl connector"):
        super().__init__(name)

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
        self.logger.info("Connection to Ardupilot established")

    def disconnect(self):
        self.process.close()
        self.logger.warning("Connector stopped")

    def get_info(self):
        run_command(self.process, "status", "VIBRATION")
        for line in self.process.before.decode().splitlines():
            if "VFR_HUD" in line:
                data_str = line.split('{', 1)[1].rsplit('}', 1)[0]
                data_dict = {}
                for item in data_str.split(','):
                    key, value = item.split(':', 1)
                    data_dict[key.strip()] = float(value.strip()) if '.' in value else int(value.strip())
                return data_dict

    def perform_action(self, action: Action):
        self.logger.info(f"Performing action {action.name}...")
        if type(action) == StopAction:
            self._stop_action()

    def _stop_action(self):
        print("STOP!!!")
