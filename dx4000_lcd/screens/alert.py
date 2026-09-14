from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

class AlertScreen:
    def render(self, alert) -> ScreenOutput:
        source = alert.source.upper()
        
        line1 = fit_line(f"! {source}!")
        line2 = fit_line(alert.message[:16])
        
        return ScreenOutput(line1=line1, line2=line2)
