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
        
        if active == 0:
            return ScreenOutput(
                line1=fit_line("TOR IDLE"),
                line2=fit_line(f"{DOWNLOAD} -- {UPLOAD} --"),
            )
        
        dl = format_speed(torrent.dl_speed)
        up = format_speed(torrent.ul_speed)
        progress = int(torrent.progress) if torrent.progress else 0
        
        if active > 1 and torrent.torrent_names:
            name = torrent.torrent_names[name_index % len(torrent.torrent_names)][:10]
        else:
            name = torrent.torrent_name[:10] if torrent.torrent_name else "TOR"
        
        return ScreenOutput(
            line1=fit_line(f"{DOWNLOAD} {dl} {progress}%"),
            line2=fit_line(f"ETA {torrent.eta or 0}s {active}T"),
        )
