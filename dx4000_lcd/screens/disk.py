from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp
from dx4000_lcd.icons import TEMP

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
        health = disk.health.upper()

        try:
            temp_val = int(temp.replace("C", "")) if temp and temp != "--C" else 0
        except ValueError:
            temp_val = 0

        if temp_val >= 45:
            return ScreenOutput(
                line1=fit_line(f"! {disk.name} HOT"),
                line2=fit_line(temp),
            )

        return ScreenOutput(
            line1=fit_line(f"{disk.name} {temp}"),
            line2=fit_line(health),
        )
