import pexpect
import sys
from pathlib import Path
from time import sleep

ARDUPILOT_DIR = Path(__file__).parent.parent
SITL_COMMAND = "./build/sitl/bin/ardurover -S -w --model rover --speedup 1 --slave 0 --defaults Tools/autotest/default_params/rover.parm --sim-address=127.0.0.1 -I0"
MAVPROXY_COMMAND = "python3 venv/bin/mavproxy.py --out 127.0.0.1:14550 --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --map"
MAVPROXY_CONTROLLER_COMMAND = "python3 venv/bin/mavproxy.py --sitl 127.0.0.1:5501"

def run_command(process, command, expected, retry=0):
    try:
        process.sendline(command)
        process.expect(expected)
        print(f"Command '{command}' succeeded")
    except pexpect.exceptions.TIMEOUT:
        retry += 1
        if retry < 2:
            print(f"Command '{command}' timed out. Repeating...")
            print(process.before.decode())
            run_command(process, command, expected, retry)
        else:
            print(f"Command '{command}' timed out. Giving up.")
            sys.exit(1)


ardurover_process = pexpect.spawn(SITL_COMMAND, cwd=ARDUPILOT_DIR)
ardurover_process.expect("Waiting for connection")
print("Ardurover started")

mavproxy_process = pexpect.spawn(MAVPROXY_COMMAND, cwd=ARDUPILOT_DIR)
mavproxy_process.expect("Detected vehicle")
print("Mavproxy started")

mavproxy_controller_process = pexpect.spawn(MAVPROXY_CONTROLLER_COMMAND, cwd=ARDUPILOT_DIR)
mavproxy_controller_process.expect("Detected vehicle")
print("Mavproxy controller started")

mavproxy_process.expect("height 588", timeout=60)
print("Mavproxy connected to Ardurover")

run_command(mavproxy_process, "module load message", "Loaded module message")
run_command(mavproxy_process, "GUIDED", "Mode GUIDED")
sleep(1)
run_command(mavproxy_process, "arm throttle", "AP: Throttle armed")

while True:
    mavproxy_process.sendline("message SET_POSITION_TARGET_LOCAL_NED 0 0 0 9 3559 0 0 0 5 0 0 0 0 0 0 0")
    mavproxy_process.expect("AP: target not received last 3secs")
    print("Sending SET_POSITION_TARGET_LOCAL_NED")

    run_command(mavproxy_controller_process, "status", "VIBRATION")
    for line in mavproxy_controller_process.before.decode().splitlines():
        if "groundspeed" in line:
            print(line)

sleep(10)
