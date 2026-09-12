from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

def format_speed(value):
    if value is None or value == 0:
        return "0B/s"
    units = ["B/s", "K/s", "M/s", "G/s"]
    v = float(value)
    for unit in units:
        if v < 1000:
            return f"{v:.1f}{unit}" if v < 100 else f"{v:.0f}{unit}"
        v /= 1000
    return f"{v:.1f}T/s"

class NetworkScreen:
    def render(self, state) -> ScreenOutput:
        rx = format_speed(state.network.rx_bps)
        tx = format_speed(state.network.tx_bps)
        return ScreenOutput(
            line1=fit_line(f"RX {rx}"),
            line2=fit_line(f"TX {tx}"),
        )
