from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_speed

class NetworkScreen:
    def render(self, state) -> ScreenOutput:
        rx = format_speed(state.network.rx_bps)
        tx = format_speed(state.network.tx_bps)
        return ScreenOutput(
            line1=fit_line(f"NET {rx}"),
            line2=fit_line(f"NET {tx}"),
        )
