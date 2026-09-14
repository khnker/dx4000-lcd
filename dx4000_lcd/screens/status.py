from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.bar import render_bar
from dx4000_lcd.formatters import format_temp
from dx4000_lcd.icons import TEMP, FAN
from dx4000_lcd.health import HealthEngine

class StatusScreen:
    def __init__(self):
        self.health_engine = HealthEngine()

    def render(self, state) -> ScreenOutput:
        cpu_val = state.cpu.temp_c.value if hasattr(state.cpu.temp_c, "value") and state.cpu.temp_c.value is not None else (state.cpu.temp_c if isinstance(state.cpu.temp_c, (int, float)) else None)
        cpu_temp = format_temp(cpu_val)

        disk_temps = [d.temp_c for d in state.disks if d.temp_c is not None]
        disk_temp = format_temp(max(disk_temps)) if disk_temps else "--C"

        fan_rpm = state.fan.rpm
        fan_text = f"{fan_rpm // 1000}K" if fan_rpm and fan_rpm >= 1000 else str(fan_rpm) if fan_rpm else "--"

        pct = round(state.storage.used_pct)
        bar = render_bar(pct, 7)

        alerts = self.health_engine.evaluate(state)
        has_warn = any(a.health.value in ("warn", "error") for a in alerts)

        if has_warn:
            return ScreenOutput(
                line1=fit_line(f"DSK {disk_temp} STO {pct}%"),
                line2=fit_line(f"! WARN"),
            )

        return ScreenOutput(
            line1=fit_line(f"{TEMP} {cpu_temp} {FAN} {fan_text}"),
            line2=fit_line(f"DSK {disk_temp} STO {pct}%"),
        )
