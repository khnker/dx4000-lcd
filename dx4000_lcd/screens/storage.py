from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.bar import render_bar
from dx4000_lcd.formatters import format_bytes

class StorageScreen:
    def render(self, state) -> ScreenOutput:
        storage = state.storage

        used = format_bytes(storage.used_bytes)
        pct = int(storage.used_pct)

        bar = render_bar(storage.used_pct, 10)

        return ScreenOutput(
            line1=fit_line(f"STO {pct}%"),
            line2=fit_line(f"{bar} {used}"),
        )
