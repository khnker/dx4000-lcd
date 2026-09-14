from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.tokens import DiskToken, TemperatureToken, StateToken
from dx4000_lcd.health import get_hottest_disk
from dx4000_lcd.layouts import layout_disk


class DiskScreen:
    def render(self, state) -> ScreenOutput:
        hottest = get_hottest_disk(state)

        if not hottest:
            return ScreenOutput(
                line1=fit_line("DISK --"),
                line2=fit_line("NO DATA"),
            )

        disk_name = DiskToken.render(hottest.name)
        temp = TemperatureToken.render(hottest.temp_c)
        health_state = StateToken.render(getattr(hottest, "health", None))

        line1, line2 = layout_disk(disk_name, temp, health_state)

        return ScreenOutput(
            line1=fit_line(line1),
            line2=fit_line(line2),
        )
