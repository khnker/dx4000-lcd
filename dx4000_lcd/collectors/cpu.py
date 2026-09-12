import logging
from dx4000_lcd.state import SystemState
from dx4000_lcd.hardware import get_temp_input

class CpuCollector:
    def __init__(self):
        self._prev_idle = None
        self._prev_total = None

    def read(self, state: SystemState):
        # Temperature from coretemp hwmon
        temp = get_temp_input("coretemp", temp_id=2)
        if temp is not None:
            state.cpu.temp_c = temp
        else:
            logging.warning("CpuCollector: could not read CPU temperature")

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
        except Exception as e:
            logging.warning(f"CpuCollector usage failed: {e}")

        # Load
        try:
            with open("/proc/loadavg") as f:
                state.cpu.load_1m = float(f.read().split()[0])
        except Exception as e:
            logging.warning(f"CpuCollector load failed: {e}")
