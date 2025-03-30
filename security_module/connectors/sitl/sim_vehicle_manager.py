import logging
from pathlib import Path

import pexpect
from core.log_formater import colored_text

ARDUPILOT_DIR = Path(__file__).parent.parent.parent.parent
SIM_VEHICLE_PY = str(ARDUPILOT_DIR / "Tools/autotest/sim_vehicle.py")


def execute_mavproxy_command(
    process,
    command,
    expected,
    timeout=5,
    max_retries=2,
    retry=0,
):
    try:
        process.sendline(command)
        process.expect(expected, timeout=timeout)
    except pexpect.exceptions.TIMEOUT as e:
        retry += 1
        if retry < max_retries:
            logging.warning(
                colored_text(
                    f"Command '{command}' timed out. Repeating...",
                    "yellow",
                )
            )
            execute_mavproxy_command(
                process,
                command,
                expected,
                timeout,
                retry,
            )
        else:
            raise pexpect.exceptions.TIMEOUT(f"Command '{command}' timed out. Giving up.") from e


class SimVehicleManager:
    def __init__(self, name: str = "sim_vehicle_manager"):
        self.name = name
        self.logger = logging.getLogger(name)

    def __del__(self):
        if hasattr(self, "process"):
            self.process.sendcontrol("C")
            self.process.close()
            self.logger.info(colored_text("Ardupilot stopped", "red"))

    def send_mavproxy_command(
        self,
        command: str,
        expected_response: str = "",
        timeout: int = 5,
    ) -> int:
        self.logger.debug(f"Sending MAVProxy command: '{command}'")
        self.process.sendline(command)
        if expected_response:
            try:
                self.process.expect(
                    expected_response,
                    timeout=timeout,
                )
            except pexpect.exceptions.TIMEOUT as e:
                self.logger.error(f"MAVProxy command '{command}' timed out")
                return 1
        self.logger.debug(f"MAVProxy command '{command}' succedded")
        return 0

    def start_simulation(self):
        self.logger.info("Starting Ardupilot...")
        self.process = pexpect.spawn(
            SIM_VEHICLE_PY,
            args=[
                "--map",
                "-v",
                "Rover",
                "--no-rebuild",
            ],
            cwd=ARDUPILOT_DIR,
        )
        try:
            self.process.expect("Detected vehicle", timeout=60)
            self.logger.info(
                colored_text(
                    "Connection to Ardupilot established",
                    "green",
                )
            )

            self.logger.info("Waiting for vehicle to load...")
            self.process.expect("height", timeout=60)
            self.logger.info(colored_text("Vehicle loaded", "green"))

            self.logger.info("Trying to arm throttle...")
            execute_mavproxy_command(
                self.process,
                "arm throttle",
                "ARMED",
                max_retries=3,
            )
            self.logger.info(colored_text("Throttle armed", "green"))

            self.logger.info("Switching to guided mode...")
            execute_mavproxy_command(
                self.process,
                "GUIDED",
                "Mode GUIDED",
                max_retries=3,
            )
            self.logger.info("Switched to guided mode")
        except pexpect.exceptions.TIMEOUT as e:
            raise RuntimeError("Unable to start Ardupilot using sim_vehicle.py") from e
