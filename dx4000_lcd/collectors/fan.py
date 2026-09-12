import logging
from dx4000_lcd.state import SystemState
from dx4000_lcd.hardware import get_fan_input, get_pwm

class FanCollector:
    def read(self, state: SystemState):
        try:
            # Using hardware discovery via hardware.py (assuming nct6683 or similar)
            # Hardcoded fan_id=2 based on previous successful tests
            state.fan.rpm = get_fan_input("nct6683", fan_id=2)
            state.fan.pwm = get_pwm("nct6683", pwm_id=2)
            state.fan.status = "VALID"
        except Exception as e:
            logging.warning(f"FanCollector failed: {e}")
            state.fan.rpm = 0
            state.fan.status = "ERROR"
