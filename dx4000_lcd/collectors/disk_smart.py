from dx4000_lcd.state import SystemState, DiskState
from dx4000_lcd.hardware import discover_disks
import subprocess
import json
import logging

class DiskSmartCollector:
    def read(self, state: SystemState):
        disks = []
        for dev in discover_disks():
            try:
                res = subprocess.run(
                    ["smartctl", "-A", "-j", dev],
                    capture_output=True, text=True, timeout=3
                )
                if res.returncode == 0:
                    data = json.loads(res.stdout)
                    temp = None
                    # Buscar atributo 194 o Temperature_Celsius
                    attrs = data.get("ata_smart_attributes", {}).get("table", [])
                    for attr in attrs:
                        if attr.get("id") == 194 or "Temperature" in attr.get("name", ""):
                            temp = attr.get("raw", {}).get("value")
                            break
                    disks.append(DiskState(name=dev.replace("/dev/", ""), temp_c=temp, health="OK" if temp is not None else "UNKNOWN"))
                else:
                    disks.append(DiskState(name=dev.replace("/dev/", ""), temp_c=None, health="UNKNOWN"))
            except Exception as e:
                logging.warning(f"DiskSmartCollector error on {dev}: {e}")
        if disks:
            state.disks = disks
