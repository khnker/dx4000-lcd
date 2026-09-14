from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_speed
from dx4000_lcd.icons import DOWNLOAD, UPLOAD

class TorrentScreen:
    def render(self, state, name_index=0) -> ScreenOutput:
        torrent = state.torrent

        if torrent is None:
            return ScreenOutput(
                line1=fit_line("TOR OFFLINE"),
                line2=fit_line("NO DATA"),
            )

        active = torrent.active_torrents or 0
        dl = format_speed(torrent.dl_speed)

        if active == 0:
            return ScreenOutput(
                line1=fit_line("TOR IDLE"),
                line2=fit_line(f"{DOWNLOAD} 0B/s"),
            )

        if torrent.dl_speed and torrent.dl_speed < 100 * 1024:
            return ScreenOutput(
                line1=fit_line("! TOR SLOW"),
                line2=fit_line(f"{DOWNLOAD} {dl}"),
            )

        return ScreenOutput(
            line1=fit_line("TOR ACTIVE"),
            line2=fit_line(f"{DOWNLOAD} {dl}"),
        )
