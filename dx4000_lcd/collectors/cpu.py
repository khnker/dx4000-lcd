import time
import logging
from dx4000_lcd.state import SystemState, TelemetryValue
from dx4000_lcd.hardware import get_temp_input

class CpuCollector:
    def __init__(self):
        self._prev_idle = None
        self._prev_total = None

    def read(self, state: SystemState):
        now = time.monotonic()
        
        temp = get_temp_input("coretemp", temp_id=3)
        if temp is not None:
            state.cpu.temp_c = TelemetryValue(value=temp, timestamp=now, status="VALID")
        else:
            state.cpu.temp_c = TelemetryValue(value=None, timestamp=now, status="ERROR")
            logging.warning("CpuCollector: could not read CPU temperature")

        try:
            with open("/proc/stat") as f:
                line = f.readline()
            parts = line.split()
            idle = int(parts[4])
            total = sum(int(p) for p in parts[1:])
            if self._prev_idle is not None:
                d_idle = idle - self._prev_idle
                d_total = total - self._prev_total
                usage = round((1 - d_idle / d_total) * 100, 1) if d_total > 0 else 0
                state.cpu.usage_pct = TelemetryValue(value=usage, timestamp=now, status="VALID")
            self._prev_idle = idle
            self._prev_total = total
        except Exception as e:
            logging.warning(f"CpuCollector usage failed: {e}")
            state.cpu.usage_pct = TelemetryValue(value=None, timestamp=now, status="ERROR")

        try:
            with open("/proc/loadavg") as f:
                load = float(f.read().split()[0])
            state.cpu.load_1m = TelemetryValue(value=load, timestamp=now, status="VALID")
        except Exception as e:
            logging.warning(f"CpuCollector load failed: {e}")
            state.cpu.load_1m = TelemetryValue(value=None, timestamp=now, status="ERROR")
