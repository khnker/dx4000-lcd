# DiskSmartCollector - reads SMART data using JSON output
import logging
from dx4000_lcd.state import SystemState, DiskState
from dx4000_lcd.hardware import discover_disks
import subprocess
import json

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
                ["/usr/sbin/smartctl", "-A", "-H", "-j", dev],
                capture_output=True, text=True, timeout=5
            )
            if not res.stdout:
                return DiskState(name=name, temp_c=None, health="NO_DATA")

            data = json.loads(res.stdout)
            
            # Get temperature from SMART attribute 194 or Temperature_Celsius
            # Use raw value (first number in the raw string), not normalized value
            temp = None
            attrs = data.get("ata_smart_attributes", {}).get("table", [])
            for attr in attrs:
                if attr.get("id") == 194 or "Temperature" in str(attr.get("name", "")):
                    raw = attr.get("raw", {})
                    raw_str = raw.get("string", "")
                    if raw_str:
                        import re
                        match = re.match(r"(\d+)", raw_str)
                        if match:
                            temp = int(match.group(1))
                    break

            # Get health status
            overall = data.get("smart_status", {}).get("passed", None)
            if overall is True:
                health = "OK"
            elif overall is False:
                health = "FAIL"
            else:
                health = "UNKNOWN"

            return DiskState(name=name, temp_c=temp, health=health)

        except subprocess.TimeoutExpired:
            return DiskState(name=name, temp_c=None, health="TIMEOUT")
        except json.JSONDecodeError:
            return DiskState(name=name, temp_c=None, health="PARSE_ERR")
        except Exception as e:
            logging.warning(f"DiskSmartCollector error on {dev}: {e}")
            return DiskState(name=name, temp_c=None, health="ERROR")
