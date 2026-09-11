import subprocess
import time
from dx4000_lcd.state import DiskState, FanState, StorageState, SystemState, CpuState, MemoryState, NetworkState


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()


class CpuCollector:
    def read(self, state: SystemState):
        # Temperatura
        try:
            with open("/sys/class/hwmon/hwmon0/temp2_input") as f:
                state.cpu.temp_c = int(f.read().strip()) // 1000
        except:
            pass

        # Usage desde /proc/stat
        try:
            with open("/proc/stat") as f:
                line = f.readline()
            parts = line.split()
            idle = int(parts[4])
            total = sum(int(p) for p in parts[1:])
            if hasattr(self, "_prev_idle"):
                d_idle = idle - self._prev_idle
                d_total = total - self._prev_total
                state.cpu.usage_pct = round((1 - d_idle / d_total) * 100, 1) if d_total > 0 else 0
            self._prev_idle = idle
            self._prev_total = total
        except:
            pass

        # Load
        try:
            with open("/proc/loadavg") as f:
                state.cpu.load_1m = float(f.read().split()[0])
        except:
            pass


class MemoryCollector:
    def read(self, state: SystemState):
        try:
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            info = {}
            for line in lines:
                parts = line.split()
                key = parts[0].rstrip(":")
                info[key] = int(parts[1])  # kB

            total = info.get("MemTotal", 0)
            avail = info.get("MemAvailable", 0)
            used = total - avail

            state.memory.total_mb = total / 1024
            state.memory.available_mb = avail / 1024
            state.memory.used_pct = round(used / total * 100, 1) if total > 0 else 0
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
        # Detectar mergerfs
        try:
            out = subprocess.run(
                ["findmnt", "-T", self.mountpoint, "-no", "FSTYPE"],
                capture_output=True, text=True, timeout=2
            ).stdout.strip()
            state.storage.mergerfs = "mergerfs" in out
        except:
            pass


class NetworkCollector:
    def __init__(self):
        self._prev_rx = 0
        self._prev_tx = 0
        self._prev_time = 0.0

    def read(self, state: SystemState):
        try:
            with open("/proc/net/dev") as f:
                lines = f.readlines()
            rx_total = 0
            tx_total = 0
            for line in lines[2:]:
                if ":" in line:
                    parts = line.split()
                    rx_total += int(parts[1])
                    tx_total += int(parts[9])

            now = time.time()
            elapsed = now - self._prev_time
            if elapsed > 0 and self._prev_time > 0:
                state.network.rx_bps = int((rx_total - self._prev_rx) / elapsed)
                state.network.tx_bps = int((tx_total - self._prev_tx) / elapsed)

            self._prev_rx = rx_total
            self._prev_tx = tx_total
            self._prev_time = now
        except:
            pass

        # IP
        try:
            out = subprocess.run(
                ["hostname", "-I"],
                capture_output=True, text=True, timeout=2
            ).stdout.strip()
            if out:
                state.network.ip = out.split()[0]
        except:
            pass


class UptimeCollector:
    def read(self, state: SystemState):
        try:
            with open("/proc/uptime") as f:
                state.uptime_seconds = int(float(f.read().split()[0]))
        except:
            pass
