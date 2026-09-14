from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_speed
from dx4000_lcd.icons import DOWNLOAD, UPLOAD

class NetworkScreen:
    def render(self, state) -> ScreenOutput:
        rx = format_speed(state.network.rx_bps)
        tx = format_speed(state.network.tx_bps)

        return ScreenOutput(
            line1=fit_line(f"{DOWNLOAD} {rx}"),
            line2=fit_line(f"{UPLOAD} {tx}"),
        )
