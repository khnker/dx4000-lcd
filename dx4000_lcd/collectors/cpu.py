import subprocess
import logging
from dx4000_lcd.state import SystemState, CpuState

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

class CpuCollector:
    def __init__(self):
        self._prev_idle = None
        self._prev_total = None
        self._last_success = 0

    def read(self, state: SystemState):
        now = self._last_success

        # Temperature
        try:
            with open("/sys/class/hwmon/hwmon0/temp2_input") as f:
                state.cpu.temp_c = int(f.read().strip()) // 1000
            self._last_success = now
        except Exception as e:
            logging.warning(f"CpuCollector temp failed: {e}")

        # Usage from /proc/stat
        try:
            with open("/proc/stat") as f:
                line = f.readline()
            parts = line.split()
            idle = int(parts[4])
            total = sum(int(p) for p in parts[1:])
            if self._prev_idle is not None:
                d_idle = idle - self._prev_idle
                d_total = total - self._prev_total
                state.cpu.usage_pct = round((1 - d_idle / d_total) * 100, 1) if d_total > 0 else 0
            self._prev_idle = idle
            self._prev_total = total
            self._last_success = now
        except Exception as e:
            logging.warning(f"CpuCollector usage failed: {e}")

        # Load
        try:
            with open("/proc/loadavg") as f:
                state.cpu.load_1m = float(f.read().split()[0])
            self._last_success = now
        except Exception as e:
            logging.warning(f"CpuCollector load failed: {e}")
