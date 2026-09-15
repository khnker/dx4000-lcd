# DiskSmartCollector - reads SMART data using JSON output
import logging
import re
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
            
            # Initialize SMART health indicators
            temp = None
            reallocated = 0
            uncorrectable = 0
            command_timeout = 0
            power_on_hours = 0
            
            attrs = data.get("ata_smart_attributes", {}).get("table", [])
            for attr in attrs:
                attr_id = attr.get("id")
                raw = attr.get("raw", {})
                raw_str = raw.get("string", "")
                raw_val = 0
                if raw_str:
                    match = re.match(r"(\d+)", raw_str)
                    if match:
                        raw_val = int(match.group(1))
                
                # Temperature (attribute 194)
                if attr_id == 194 or "Temperature" in str(attr.get("name", "")):
                    temp = raw_val
                # Reallocated sectors (attribute 5)
                elif attr_id == 5:
                    reallocated = raw_val
                # Uncorrectable errors (attribute 187)
                elif attr_id == 187:
                    uncorrectable = raw_val
                # Command timeout (attribute 188)
                elif attr_id == 188:
                    command_timeout = raw_val
                # Power-on hours (attribute 9)
                elif attr_id == 9:
                    power_on_hours = raw_val

            # Get health status
            overall = data.get("smart_status", {}).get("passed", None)
            if overall is True:
                health = "OK"
            elif overall is False:
                health = "FAIL"
            else:
                health = "UNKNOWN"

            # Downgrade health if critical SMART attributes are bad
            if uncorrectable > 0 or command_timeout > 100:
                health = "CRITICAL"
            elif reallocated > 0 or power_on_hours > 52560:
                health = "DEGRADED" if health == "OK" else health

            return DiskState(
                name=name,
                temp_c=temp,
                health=health,
                reallocated=reallocated,
                uncorrectable=uncorrectable,
                command_timeout=command_timeout,
                power_on_hours=power_on_hours
            )

        except subprocess.TimeoutExpired:
            return DiskState(name=name, temp_c=None, health="TIMEOUT")
        except json.JSONDecodeError:
            return DiskState(name=name, temp_c=None, health="PARSE_ERR")
        except Exception as e:
            logging.warning(f"DiskSmartCollector error on {dev}: {e}")
            return DiskState(name=name, temp_c=None, health="ERROR")
