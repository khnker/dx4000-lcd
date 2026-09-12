# FanCollector - reads fan RPM and PWM using hardware discovery
import logging
from dx4000_lcd.state import SystemState
from dx4000_lcd.hardware import get_fan_input, get_pwm, find_hwmon

class FanCollector:
    def __init__(self):
        self._hwmon_name = "nct6683"  # NCT6683 super I/O chip on DX4000

    def read(self, state: SystemState):
        # Try NCT6683 first (DX4000 has this super I/O)
        rpm = get_fan_input(self._hwmon_name, fan_id=2)
        if rpm is None:
            # Fallback: try coretemp hwmon for fan
            rpm = get_fan_input("coretemp", fan_id=2)
        
        pwm = get_pwm(self._hwmon_name, pwm_id=2)
        if pwm is None:
            pwm = get_pwm("coretemp", pwm_id=2)

        if rpm is not None:
            state.fan.rpm = rpm
        else:
            logging.warning("FanCollector: could not read fan RPM")

        state.fan.pwm = pwm
