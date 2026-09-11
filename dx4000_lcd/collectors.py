import subprocess
import time
from typing import Optional

from dx4000_lcd.models.state import NasState, DiskHealth, FanStatus, StorageStatus


def read_cpu() -> int:
    try:
        with open("/sys/class/hwmon/hwmon0/temp2_input") as f:
            return int(f.read().strip()) // 1000
    except:
        return 0


def read_fan() -> FanStatus:
    status = FanStatus()
    try:
        with open("/sys/class/hwmon/hwmon1/pwm2") as f:
            status.pwm = int(f.read().strip())
    except:
        pass
    try:
        with open("/sys/class/hwmon/hwmon1/fan2_input") as f:
            status.rpm = int(f.read().strip())
    except:
        pass
    return status


def read_disks() -> list:
    devices = ["/dev/sda", "/dev/sdb", "/dev/sdd", "/dev/sde", "/dev/sdf"]
    disks = []
    for dev in devices:
        temp = None
        try:
            out = subprocess.run(
                ["smartctl", "-A", dev],
                capture_output=True, text=True, timeout=2
            ).stdout
            for line in out.splitlines():
                if "Temperature_Celsius" in line:
                    parts = line.split()
                    temp = int(parts[len(parts)-1])
                    break
        except:
            pass
        disks.append(DiskHealth(device=dev.replace("/dev/", ""), temperature_c=temp))
    return disks


def read_storage() -> StorageStatus:
    status = StorageStatus()
    try:
        total = used = 0
        out = subprocess.run(
            ["df", "-P", "-x", "tmpfs", "-x", "devtmpfs"],
            capture_output=True, text=True
        ).stdout
        for line in out.splitlines()[1:]:
            cols = line.split()
            if len(cols) >= 4 and cols[0].startswith("/dev/sd"):
                used += int(cols[2]) * 1024
                total += int(cols[1]) * 1024
        status.total_bytes = total
        status.used_bytes = used
        status.percent_used = int(used * 100 / total) if total else 0
    except:
        pass
    return status


def collect() -> NasState:
    state = NasState()
    state.cpu.temp_c = read_cpu()
    state.fan = read_fan()
    state.disks = read_disks()
    state.storage = read_storage()
    return state