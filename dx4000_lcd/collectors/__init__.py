import subprocess
import time
from dx4000_lcd.state import DiskState, FanState, StorageState, SystemState


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()


class CpuCollector:
    def read(self, state: SystemState):
        try:
            with open("/sys/class/hwmon/hwmon0/temp2_input") as f:
                state.cpu.temp_c = int(f.read().strip()) // 1000
        except:
            pass


class FanCollector:
    def read(self, state: SystemState):
        try:
            with open("/sys/class/hwmon/hwmon1/pwm2") as f:
                state.fan.pwm = int(f.read().strip())
        except:
            pass
        try:
            with open("/sys/class/hwmon/hwmon1/fan2_input") as f:
                state.fan.rpm = int(f.read().strip())
        except:
            pass


class DiskTempCollector:
    DEVICES = ["/dev/sda", "/dev/sdb", "/dev/sdd", "/dev/sde", "/dev/sdf"]

    def read(self, state: SystemState):
        state.disks = []
        for dev in self.DEVICES:
            name = dev.replace("/dev/", "")
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
            state.disks.append(DiskState(name=name, temp_c=temp))


class StorageCollector:
    def __init__(self, mountpoint="/mnt/media"):
        self.mountpoint = mountpoint

    def read(self, state: SystemState):
        try:
            out = subprocess.run(
                ["df", "-B1", self.mountpoint],
                capture_output=True, text=True, timeout=2
            ).stdout
            lines = out.strip().splitlines()
            if len(lines) >= 2:
                cols = lines[1].split()
                state.storage.total_bytes = int(cols[1])
                state.storage.used_bytes = int(cols[2])
                state.storage.free_bytes = int(cols[3])
        except:
            pass
