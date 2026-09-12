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
    """Discover all block devices that are physical disks (not partitions)."""
    disks = []
    for path in Path("/sys/block").iterdir():
        name = path.name
        # Skip loop, ram, and partition devices
        if name.startswith(("loop", "ram", "zram")):
            continue
        # Only include sdX, nvmeXn1, etc.
        if name.startswith(("sd", "nvme", "vd", "hd")):
            # Skip partitions (e.g., sda1)
            if name[-1].isdigit() and not name[:-1].endswith("p"):
                continue
            disks.append(f"/dev/{name}")
    return sorted(disks)

def discover_all_devices() -> list[str]:
    """Discover all block devices including partitions."""
    devices = []
    for path in Path("/sys/block").iterdir():
        name = path.name
        if name.startswith(("loop", "ram", "zram")):
            continue
        devices.append(f"/dev/{name}")
    return sorted(devices)

def get_all_hwmon_devices() -> Dict[str, Path]:
    devices = {}
    for path in Path("/sys/class/hwmon").glob("hwmon*"):
        try:
            name = (path / "name").read_text().strip()
            devices[name] = path
        except OSError:
            continue
    return devices
