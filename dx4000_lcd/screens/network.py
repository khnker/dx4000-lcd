from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.tokens import SpeedToken
from dx4000_lcd.icons import DOWNLOAD, UPLOAD


class NetworkScreen:
    def render(self, state) -> ScreenOutput:
        rx = SpeedToken.render(getattr(state.network, "rx_bps", 0))
        tx = SpeedToken.render(getattr(state.network, "tx_bps", 0))

        return ScreenOutput(
            line1=fit_line(f"{DOWNLOAD} {rx}"),
            line2=fit_line(f"{UPLOAD} {tx}"),
        )
