# UptimeCollector - reads system uptime
import logging
from dx4000_lcd.state import SystemState

class UptimeCollector:
    def read(self, state: SystemState):
        try:
            with open("/proc/uptime") as f:
                seconds = float(f.read().split()[0])
            
            days = int(seconds // 86400)
            hours = int((seconds % 86400) // 3600)
            mins = int((seconds % 3600) // 60)
            
            state.uptime.seconds = int(seconds)
            state.uptime.days = days
            state.uptime.hours = hours
            state.uptime.minutes = mins
        except Exception as e:
            logging.warning(f"UptimeCollector failed: {e}")
