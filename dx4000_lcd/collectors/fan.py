import subprocess
import logging
from dx4000_lcd.state import SystemState, FanState

class FanCollector:
    def __init__(self):
        self._last_success = 0

    def read(self, state: SystemState):
        try:
            with open("/sys/class/hwmon/hwmon1/fan2_input") as f:
                state.fan.rpm = int(f.read().strip())
            self._last_success = self._last_success
        except Exception as e:
            logging.warning(f"FanCollector failed: {e}")
            state.fan.rpm = 0

        try:
            with open("/sys/class/hwmon/hwmon1/pwm2") as f:
                state.fan.pwm = int(f.read().strip())
        except Exception as e:
            logging.warning(f"FanCollector PWM failed: {e}")
            state.fan.pwm = None
