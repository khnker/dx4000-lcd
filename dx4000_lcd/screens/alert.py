from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

class AlertScreen:
    def render(self, alert) -> ScreenOutput:
        source = alert.source.upper()
        msg = alert.message
        
        if source == "disk":
            line1 = fit_line(f"!! DISK HOT!!")
        elif source == "cpu":
            line1 = fit_line(f"!! CPU HOT!!")
        elif source == "fan":
            line1 = fit_line(f"!! FAN ERROR!!")
        elif source == "storage":
            line1 = fit_line(f"!! STORAGE!!")
        else:
            line1 = fit_line(f"!! {source}!!")
        
        line2 = fit_line(msg)
        
        return ScreenOutput(line1=line1, line2=line2)
