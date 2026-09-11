from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_speed

class TorrentScreen:
    def render(self, state) -> ScreenOutput:
        name = state.torrent.torrent_name[:12] if state.torrent.torrent_name else "--"
        dl = format_speed(state.torrent.dl_speed)
        
        if state.torrent.active_torrents > 0:
            return ScreenOutput(
                line1=fit_line(f"TOR {name}"),
                line2=fit_line(f"DL {dl}"),
            )
        return ScreenOutput(
            line1=fit_line("TOR IDLE"),
            line2=fit_line(""),
        )
