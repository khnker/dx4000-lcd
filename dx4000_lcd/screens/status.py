from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.bar import render_bar
from dx4000_lcd.formatters import format_temp
from dx4000_lcd.icons import TEMP, FAN

class StatusScreen:
    def render(self, state) -> ScreenOutput:
        cpu_val = state.cpu.temp_c.value if hasattr(state.cpu.temp_c, "value") else state.cpu.temp_c
        cpu_temp = format_temp(cpu_val)

        fan = state.fan.rpm or 0
        fan_val = fan.value if hasattr(fan, 'value') else fan
        fan_text = f"{fan_val // 1000}K" if isinstance(fan_val, int) and fan_val >= 1000 else str(fan_val)

        disk_temps = [d.temp_c for d in state.disks if d.temp_c is not None]
        disk_temp = format_temp(max(disk_temps)) if disk_temps else "--C"

        pct = round(state.storage.used_pct)

        return ScreenOutput(
            line1=fit_line(f"CPU {TEMP}{cpu_temp} {FAN}{fan_text} RPM"),
            line2=fit_line(f"DSK {TEMP}{disk_temp} STO {render_bar(pct, 7)} {pct}%"),
        )