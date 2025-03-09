import logging
from pathlib import Path

import pexpect

ARDUPILOT_DIR = Path(__file__).parent.parent.parent
SIM_VEHICLE_PY = str(ARDUPILOT_DIR / "Tools/autotest/sim_vehicle.py")


class ArdupilotManager:
    def __init__(self, name: str = "Ardupilot Manager"):
        self.name = name
        self.logger = logging.getLogger(name)

    def __del__(self):
        self.process.close()
        self.logger.info("Ardupilot stopped")

    def start_simulation(self):
        self.logger.info("Starting Ardupilot...")
        self.process = pexpect.spawn(SIM_VEHICLE_PY, args=["--map", "-v", "Rover"], cwd=ARDUPILOT_DIR)
        try:
            self.process.expect("Detected vehicle", timeout=60)
            self.logger.info("Connection to Ardupilot established")

            self.logger.info("Waiting for vehicle to load...")
            self.process.expect("height", timeout=60)
            self.logger.info("Vehicle loaded")

            self.logger.info("Trying to arm throttle...")
            self.process.sendline("arm throttle")
            self.process.expect("ARMED", timeout=5)
            self.logger.info("Throttle armed")

            self.logger.info("Switching to guided mode...")
            self.process.sendline("GUIDED")
            self.process.expect("Mode GUIDED", timeout=5)
            self.logger.info("Switched to guided mode")
        except pexpect.exceptions.TIMEOUT as e:
            raise RuntimeError("Unable to start Ardupilot using sim_vehicle.py") from e
