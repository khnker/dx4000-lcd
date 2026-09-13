import logging
from dx4000_lcd.state import SystemState
from dx4000_lcd.hardware import get_fan_input, get_pwm

class FanCollector:
    def read(self, state: SystemState):
        try:
            rpm = get_fan_input("nct6683", fan_id=2)
            pwm = get_pwm("nct6683", pwm_id=2)
            
            if rpm is not None:
                state.fan.rpm = rpm
                state.fan.status = "OK"
            elif pwm is not None:
                state.fan.rpm = pwm
                state.fan.status = "PWM"
            else:
                state.fan.rpm = 0
                state.fan.status = "NO_DATA"
        except Exception as e:
            logging.warning(f"FanCollector failed: {e}")
            state.fan.rpm = 0
            state.fan.status = "ERROR"
