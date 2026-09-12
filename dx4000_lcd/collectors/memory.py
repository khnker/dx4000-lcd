# MemoryCollector - reads from /proc/meminfo
import logging
from dx4000_lcd.state import SystemState

class MemoryCollector:
    def read(self, state: SystemState):
        try:
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            info = {}
            for line in lines:
                parts = line.split()
                key = parts[0].rstrip(":")
                if len(parts) >= 2:
                    info[key] = int(parts[1])  # kB
            
            total = info.get("MemTotal", 0)
            avail = info.get("MemAvailable", 0)
            used = total - avail
            
            state.memory.total_mb = total / 1024
            state.memory.available_mb = avail / 1024
            state.memory.used_pct = round(used / total * 100, 1) if total > 0 else 0
        except Exception as e:
            logging.warning(f"MemoryCollector failed: {e}")
