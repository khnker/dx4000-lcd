from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

def format_temp(value):
    if value is None:
        return "--"
    return f"{value:02d}C"

def format_pct(value):
    if value is None:
        return "--"
    return f"{int(value)}%"

class StatusScreen:
    def render(self, state) -> ScreenOutput:
        cpu = format_temp(state.cpu.temp_c)
        disk_temps = [d.temp_c for d in state.disks if d.temp_c is not None]
        disk = format_temp(max(disk_temps)) if disk_temps else "--"
        
        sto = format_pct(state.storage.used_pct)
        fan = state.fan.rpm if state.fan.rpm else "--"
        if fan != "--":
            fan = f"{fan // 1000:.1f}K" if fan >= 1000 else str(fan)
        
        return ScreenOutput(
            line1=fit_line(f"CPU {cpu} D{disk}"),
            line2=fit_line(f"STO {sto}% F{fan}"),
        )
