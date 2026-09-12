from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

class AlertScreen:
    def render(self, alert) -> ScreenOutput:
        source = alert.source.upper()
        
        # Detailed messages based on source
        if source == "DISK":
            line1 = fit_line("!! DISK HOT!!")
            line2 = fit_line(alert.message[:16])
        elif source == "CPU":
            line1 = fit_line("!! CPU HOT!!")
            line2 = fit_line(alert.message[:16])
        elif source == "FAN":
            line1 = fit_line("!! FAN ERROR!!")
            line2 = fit_line(alert.message[:16])
        elif source == "STORAGE":
            line1 = fit_line("!! STORAGE!!")
            line2 = fit_line(alert.message[:16])
        else:
            line1 = fit_line(f"!! {source}!!")
            line2 = fit_line(alert.message[:16] if alert.message else "CHECK")
        
        return ScreenOutput(line1=line1, line2=line2)
