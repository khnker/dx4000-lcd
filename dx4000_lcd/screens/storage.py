from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

class StorageScreen:
    def render(self, state) -> ScreenOutput:
        pct = round(state.storage.used_pct)
        total_tb = state.storage.total_bytes / (1024**4)
        used_tb = state.storage.used_bytes / (1024**4)
        
        return ScreenOutput(
            line1=fit_line(f"STO {pct}%"),
            line2=fit_line(f"{used_tb:.1f}T/{total_tb:.1f}T"),
        )
