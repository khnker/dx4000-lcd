from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

class AlertScreen:
    def render(self, alert) -> ScreenOutput:
        return ScreenOutput(
            line1=fit_line(f"! {alert.message}"),
            line2=fit_line(f"CHECK {alert.source}"),
        )