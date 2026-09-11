from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp

class StatusScreen:
    def render(self, state) -> ScreenOutput:
        cpu = format_temp(state.cpu.temp_c)
        disk_temps = [d.temp_c for d in state.disks if d.temp_c is not None]
        disk = format_temp(max(disk_temps)) if disk_temps else "--"

        pct = round(state.storage.used_pct)

        return ScreenOutput(
            line1=fit_line(f"NAS {cpu} {disk}"),
            line2=fit_line(f"STO {pct}%"),
        )
