from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp

class DiskScreen:
    def render(self, state) -> ScreenOutput:
        if not state.disks:
            return ScreenOutput(line1="NO DISKS", line2="")
        
        disk = state.disks[0]
        temp = format_temp(disk.temp_c)
        return ScreenOutput(
            line1=fit_line(f"DISK {disk.name}"),
            line2=fit_line(f"TEMP {temp}"),
        )
