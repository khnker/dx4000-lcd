from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_speed
from dx4000_lcd.icons import PLAY, PAUSE, STOP

class TorrentScreen:
    def render(self, state, name_index=0) -> ScreenOutput:
        torrent = state.torrent

        if torrent is None:
            return ScreenOutput(
                line1=fit_line(f"{STOP} TOR OFFLINE"),
                line2=fit_line("QBIT ERROR"),
            )

        if torrent.active_torrents == 0:
            return ScreenOutput(
                line1=fit_line(f"{STOP} TOR IDLE"),
                line2=fit_line("NO DOWNLOAD"),
            )

        if torrent.torrent_names and len(torrent.torrent_names) > 1:
            name = torrent.torrent_names[name_index % len(torrent.torrent_names)][:12]
        else:
            name = torrent.torrent_name[:12] if torrent.torrent_name else "TOR"

        dl = format_speed(torrent.dl_speed)
        progress = int(torrent.progress)

        if torrent.eta > 0:
            hours, remainder = divmod(torrent.eta, 3600)
            minutes = remainder // 60

            if hours:
                eta = f"{hours}H{minutes:02d}"
            else:
                eta = f"{minutes}M"
        else:
            eta = "--"

        return ScreenOutput(
            line1=fit_line(f"{PLAY} {name}"),
            line2=fit_line(f"DL {dl} {progress}% ETA {eta}"),
        )
