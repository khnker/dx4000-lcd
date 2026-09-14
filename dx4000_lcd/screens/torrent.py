from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_speed
from dx4000_lcd.icons import DOWNLOAD

STOP = "■"
PLAY = "▶"


class TorrentScreen:
    def render(self, state) -> ScreenOutput:
        torrent = getattr(state, "torrent", None)

        if torrent is None:
            return ScreenOutput(
                line1=fit_line(f"{STOP} TOR OFFLINE"),
                line2=fit_line("QBIT ERROR"),
            )

        active = torrent.active_torrents or 0
        dl = format_speed(getattr(torrent, "dl_speed", 0) or 0)

        if active == 0:
            return ScreenOutput(
                line1=fit_line(f"{STOP} TOR IDLE"),
                line2=fit_line("NO DOWNLOAD"),
            )

        if torrent.dl_speed and torrent.dl_speed < 100 * 1024:
            return ScreenOutput(
                line1=fit_line("! TOR SLOW"),
                line2=fit_line(f"{DOWNLOAD} {dl}"),
            )

        count = f" {active}" if active else ""
        return ScreenOutput(
            line1=fit_line(f"{PLAY} TOR{count} ACTIVE"),
            line2=fit_line(f"{DOWNLOAD} {dl}"),
        )
