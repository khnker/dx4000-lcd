from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_speed
from dx4000_lcd.icons import DOWNLOAD

STOP = "■"
PLAY = "▶"


class TorrentScreen:
    def render(self, state, name_index=0) -> ScreenOutput:
        del name_index
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

        count = f" {active}" if active else ""
        return ScreenOutput(
            line1=fit_line(f"{PLAY} TOR{count} ACTIVE"),
            line2=fit_line(f"{DOWNLOAD} {dl}"),
        )
