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
    def read(self, state: SystemState):
        try:
            total = used = 0
            for ln in sh("df -P -x tmpfs -x devtmpfs").splitlines()[1:]:
                c = ln.split()
                if len(c) >= 4 and c[0].startswith("/dev/sd"):
                    used += int(c[2]) * 1024
                    total += int(c[1]) * 1024
            state.storage.total_bytes = total
            state.storage.used_bytes = used
        except:
            pass
