from dx4000_lcd.state import SystemState, DiskState
from dx4000_lcd.hardware import discover_disks
import subprocess
import json
import logging

class DiskSmartCollector:
    def read(self, state: SystemState):
        disks = []
        for dev in discover_disks():
            result = self._read_disk_smart(dev)
            if result:
                disks.append(result)
        if disks:
            state.disks = disks

    def _read_disk_smart(self, dev: str) -> DiskState | None:
        name = dev.replace("/dev/", "")
        try:
            res = subprocess.run(
                ["smartctl", "-A", "-j", dev],
                capture_output=True, text=True, timeout=5
            )
            # SMART can return data even with non-zero exit codes
            if not res.stdout:
                logging.warning(f"DiskSmartCollector: no output from {dev}")
                return DiskState(name=name, temp_c=None, health="UNKNOWN")

            data = json.loads(res.stdout)
            
            # Get temperature
            temp = None
            attrs = data.get("ata_smart_attributes", {}).get("table", [])
            for attr in attrs:
                if attr.get("id") == 194 or "Temperature" in attr.get("name", ""):
                    temp = attr.get("raw", {}).get("value")
                    break

            # Get SMART health status
            overall = data.get("smart_status", {}).get("passed", None)
            if overall is True:
                health = "OK"
            elif overall is False:
                health = "FAIL"
            else:
                # Check power_on_hours as fallback indicator
                power_on = None
                for attr in attrs:
                    if attr.get("id") == 9:  # Power-On Hours
                        power_on = attr.get("raw", {}).get("value")
                if power_on is not None and power_on > 0:
                    health = "OK"
                else:
                    health = "UNKNOWN"

            return DiskState(name=name, temp_c=temp, health=health)

        except subprocess.TimeoutExpired:
            logging.warning(f"DiskSmartCollector: timeout on {dev}")
            return DiskState(name=name, temp_c=None, health="TIMEOUT")
        except json.JSONDecodeError as e:
            logging.warning(f"DiskSmartCollector: JSON parse error on {dev}: {e}")
            return DiskState(name=name, temp_c=None, health="PARSE_ERROR")
        except Exception as e:
            logging.warning(f"DiskSmartCollector error on {dev}: {e}")
            return DiskState(name=name, temp_c=None, health="ERROR")
