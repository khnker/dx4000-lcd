from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.bar import render_bar

def format_bytes(value):
    if value is None or value == 0:
        return "--"
    tb = value / (1024**4)
    return f"{tb:.1f}T"

class StorageScreen:
    def render(self, state) -> ScreenOutput:
        pct = state.storage.used_pct
        if pct is None:
            pct = 0
        
        bar = render_bar(pct, 10)
        
        total = format_bytes(state.storage.total_bytes)
        used = format_bytes(state.storage.used_bytes)
        
        return ScreenOutput(
            line1=fit_line(f"STORAGE {int(pct)}%"),
            line2=fit_line(f"{bar} {used}/{total}"),
        )
