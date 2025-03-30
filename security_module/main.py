import argparse
import logging

from connectors.sitl.sim_vehicle_manager import (
    SimVehicleManager,
)
from core.security_module import SecurityModule


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s]: %(message)s",
    datefmt="%H:%M:%S",
)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Модуль безопасности, осуществляющий контроль за соблюдением заданных политик автопилотом Ardurover"
    )
    argparser.add_argument(
        "--no-ardupilot",
        help="Не запускать Ardupilot автоматически (для ручной работы с sim_vehicle.py)",
        action="store_true",
        default=False,
    )
    argparser.parse_args()

    if not argparser.parse_args().no_ardupilot:
        am = SimVehicleManager()
        sm = SecurityModule(
            sv_manager=am,
            route_file_path="/Users/hellcat/workspace/ardupilot/security_module/route.json",
            security_file_path="/Users/hellcat/workspace/ardupilot/security_module/security.json",
        )
    else:
        sm = SecurityModule(
            route_file_path="/Users/hellcat/workspace/ardupilot/security_module/route.json",
            security_file_path="/Users/hellcat/workspace/ardupilot/security_module/security.json",
        )

    am.start_simulation()
    sm.run()
