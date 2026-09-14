from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

class AlertScreen:
    def render(self, alert) -> ScreenOutput:
        source = alert.source.upper()

        if source == "DISK":
            line1 = fit_line("!! DISK HOT!!")
        elif source == "CPU":
            line1 = fit_line("!! CPU HOT!!")
        elif source == "FAN":
            line1 = fit_line("!! FAN ERROR!!")
        elif source == "STORAGE":
            line1 = fit_line("!! STORAGE!!")
        else:
            line1 = fit_line(f"!! {source}!!")

        line2 = fit_line(alert.message[:16] if alert.message else "CHECK")

        return ScreenOutput(line1=line1, line2=line2)