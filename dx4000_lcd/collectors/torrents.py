# TorrentCollector - reads from qBittorrent API
import logging
import requests
from dx4000_lcd.state import SystemState, TorrentState

class TorrentCollector:
    def __init__(self, host="http://localhost:8080", user="admin", passwd="adminadmin"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self._session = requests.Session()
        self._logged_in = False

    def read(self, state: SystemState):
        try:
            # Login if needed
            if not self._logged_in:
                login_url = f"{self.host}/api/v2/auth/login"
                resp = self._session.post(login_url, data={"username": self.user, "password": self.passwd}, timeout=5)
                self._logged_in = resp.status_code == 200 and "Ok" in resp.text
            
            if not self._logged_in:
                state.torrent = TorrentState(status="OFFLINE", torrent_name="qBIT DOWN")
                return

            # Get torrent info
            info_url = f"{self.host}/api/v2/torrents/info"
            resp = self._session.get(info_url, timeout=5)
            if resp.status_code != 200:
                state.torrent = TorrentState(status="OFFLINE", torrent_name="API ERROR")
                return

            torrents = resp.json()
            if not torrents:
                state.torrent = TorrentState(status="IDLE", torrent_name="0 ACTIVE")
                return

            # Get most interesting torrent (downloading or with most progress)
            active = [t for t in torrents if t.get("state") in ["downloading", "uploading"]]
            if not active:
                state.torrent = TorrentState(status="IDLE", torrent_name=f"{len(torrents)} TORRENTS")
                return

            t = active[0]
            name = t.get("name", "unknown")[:12]
            dl = t.get("dlspeed", 0)
            up = t.get("upspeed", 0)
            progress = t.get("progress", 0) * 100
            
            state.torrent = TorrentState(
                status="DOWNLOADING",
                torrent_name=name,
                download_speed=dl,
                upload_speed=up,
                progress=progress
            )
        except requests.Timeout:
            state.torrent = TorrentState(status="OFFLINE", torrent_name="TIMEOUT")
        except Exception as e:
            logging.warning(f"TorrentCollector failed: {e}")
            state.torrent = TorrentState(status="OFFLINE", torrent_name="ERROR")
