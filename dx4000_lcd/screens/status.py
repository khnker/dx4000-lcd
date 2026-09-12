from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.bar import render_bar

def format_temp(value):
    if value is None:
        return "--"
    return f"{value:02d}C"

class StatusScreen:
    def render(self, state) -> ScreenOutput:
        cpu = format_temp(state.cpu.temp_c)
        
        # Get hottest disk
        disk_temps = [d.temp_c for d in state.disks if d.temp_c is not None]
        disk = format_temp(max(disk_temps)) if disk_temps else "--"
        
        # Storage: handle None properly
        used_pct = state.storage.used_pct
        if used_pct is None:
            sto_pct = "--"
            bar = "-------"
        else:
            sto_pct = f"{int(used_pct)}%"
            bar = render_bar(used_pct, 7)

        # Fan
        fan_rpm = state.fan.rpm
        if fan_rpm is None or fan_rpm == 0:
            fan = "--"
        elif fan_rpm >= 1000:
            fan = f"{fan_rpm // 1000}K"
        else:
            fan = str(fan_rpm)

        return ScreenOutput(
            line1=fit_line(f"CPU {cpu} D{disk}"),
            line2=fit_line(f"STO {bar} {sto_pct}"),
        )
