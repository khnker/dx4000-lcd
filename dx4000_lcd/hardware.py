from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

def find_hwmon(name: str) -> Optional[Path]:
    for path in Path("/sys/class/hwmon").glob("hwmon*"):
        try:
            if (path / "name").read_text().strip() == name:
                return path
        except OSError:
            continue
    return None

def get_temp_input(hwmon_name: str, temp_id: int = 2) -> Optional[int]:
    hwmon = find_hwmon(hwmon_name)
    if hwmon:
        try:
            path = hwmon / f"temp{temp_id}_input"
            if path.exists():
                return int(path.read_text().strip()) // 1000
        except (OSError, ValueError) as e:
            logger.warning(f"Failed to read temp from {hwmon_name}: {e}")
    return None

def get_fan_input(hwmon_name: str, fan_id: int = 2) -> Optional[int]:
    hwmon = find_hwmon(hwmon_name)
    if hwmon:
        try:
            path = hwmon / f"fan{fan_id}_input"
            if path.exists():
                return int(path.read_text().strip())
        except (OSError, ValueError) as e:
            logger.warning(f"Failed to read fan from {hwmon_name}: {e}")
    return None

def get_pwm(hwmon_name: str, pwm_id: int = 2) -> Optional[int]:
    hwmon = find_hwmon(hwmon_name)
    if hwmon:
        try:
            path = hwmon / f"pwm{pwm_id}"
            if path.exists():
                return int(path.read_text().strip())
        except (OSError, ValueError) as e:
            logger.warning(f"Failed to read PWM from {hwmon_name}: {e}")
    return None

def discover_disks() -> list[str]:
    return [str(p) for p in sorted(Path("/dev").glob("sd[a-z]"))]

def get_all_hwmon_devices() -> Dict[str, Path]:
    devices = {}
    for path in Path("/sys/class/hwmon").glob("hwmon*"):
        try:
            name = (path / "name").read_text().strip()
            devices[name] = path
        except OSError:
            continue
    return devices
