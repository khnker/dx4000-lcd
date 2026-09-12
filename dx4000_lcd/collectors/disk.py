import subprocess
import logging
from dx4000_lcd.state import SystemState, DiskState

DEVICES = ["/dev/sda", "/dev/sdb", "/dev/sdd", "/dev/sde", "/dev/sdf"]

class DiskTempCollector:
    def __init__(self):
        self._last_success = 0

    def read(self, state: SystemState):
        state.disks.clear()
        for dev in DEVICES:
            try:
                result = subprocess.run(
                    ["smartctl", "-A", dev],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                for line in result.stdout.splitlines():
                    if "Temperature_Celsius" in line:
                        temp = line.split()[9]
                        if temp.isdigit():
                            state.disks.append(DiskState(name=dev[-3:], temp_c=int(temp)))
                            break
                else:
                    state.disks.append(DiskState(name=dev[-3:], temp_c=None))
                self._last_success = self._last_success
            except subprocess.TimeoutExpired:
                logging.warning(f"DiskTempCollector timeout on {dev}")
                state.disks.append(DiskState(name=dev[-3:], temp_c=None))
            except Exception as e:
                logging.warning(f"DiskTempCollector failed on {dev}: {e}")
                state.disks.append(DiskState(name=dev[-3:], temp_c=None))
