from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.tokens import StateToken, CountToken, SpeedToken


class TorrentScreen:
    def render(self, state) -> ScreenOutput:
        torrent = getattr(state, "torrent", None)

        if torrent is None:
            return ScreenOutput(
                line1=fit_line("TOR OFFLINE"),
                line2=fit_line("NO DATA"),
            )

        active = torrent.active_torrents or 0

        if active == 0:
            return ScreenOutput(
                line1=fit_line("TOR IDLE"),
                line2=fit_line(f"DOWN {SpeedToken.render(0)}"),
            )

        if getattr(torrent, "dl_speed", 0) and torrent.dl_speed < 100 * 1024:
            return ScreenOutput(
                line1=fit_line("! TOR SLOW"),
                line2=fit_line(f"DOWN {SpeedToken.render(torrent.dl_speed)}"),
            )

        return ScreenOutput(
            line1=fit_line(f"TOR {CountToken.render(active)} ACTIVE"),
            line2=fit_line(f"DOWN {SpeedToken.render(torrent.dl_speed)}"),
        )
