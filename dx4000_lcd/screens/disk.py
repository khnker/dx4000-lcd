from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp
from dx4000_lcd.icons import THERMO

class DiskScreen:
    def render(self, state) -> ScreenOutput:
        if not state.disks:
            return ScreenOutput(
                line1=fit_line("DISK --"),
                line2=fit_line("NO DATA"),
            )
        
        disk = max(
            state.disks,
            key=lambda d: d.temp_c if d.temp_c is not None else -1,
        )
        
        temp = format_temp(disk.temp_c)
        
        return ScreenOutput(
            line1=fit_line(f"{disk.name} {THERMO}{temp}"),
            line2=fit_line(f"SMART {disk.health}"),
        )
