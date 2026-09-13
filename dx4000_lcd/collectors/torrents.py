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
            if not self._logged_in:
                try:
                    login_url = f"{self.host}/api/v2/auth/login"
                    resp = self._session.post(login_url, data={"username": self.user, "password": self.passwd}, timeout=5)
                    self._logged_in = resp.status_code == 200 and "Ok" in resp.text
                except:
                    self._logged_in = False

            if not self._logged_in:
                state.torrent = TorrentState(
                    torrent_name="OFFLINE",
                    torrent_names=[],
                    dl_speed=0,
                    ul_speed=0,
                    active_torrents=0,
                    progress=0.0,
                    eta=0
                )
                return

            info_url = f"{self.host}/api/v2/torrents/info"
            resp = self._session.get(info_url, timeout=5)
            if resp.status_code != 200:
                raise Exception("API error")

            torrents = resp.json()
            if not torrents:
                state.torrent = TorrentState(
                    torrent_name="IDLE",
                    torrent_names=[],
                    dl_speed=0,
                    ul_speed=0,
                    active_torrents=0,
                    progress=0.0,
                    eta=0
                )
                return

            all_names = [t.get("name", "") for t in torrents if t.get("name")]
            active = [t for t in torrents if t.get("state") in ["downloading", "uploading"]]

            if not active:
                state.torrent = TorrentState(
                    torrent_name="IDLE",
                    torrent_names=all_names,
                    dl_speed=0,
                    ul_speed=0,
                    active_torrents=len(torrents),
                    progress=0.0,
                    eta=0
                )
                return

            t = active[0]
            dl_speed = t.get("dlspeed", 0)
            ul_speed = t.get("upspeed", 0)
            progress = t.get("progress", 0.0) * 100
            eta = t.get("eta", -1)

            state.torrent = TorrentState(
                torrent_name=t.get("name", "Unknown"),
                torrent_names=all_names,
                dl_speed=dl_speed,
                ul_speed=ul_speed,
                active_torrents=len(active),
                progress=progress,
                eta=eta
            )

        except Exception as e:
            logging.warning(f"TorrentCollector failed: {e}")
            state.torrent = TorrentState(
                torrent_name="ERROR",
                torrent_names=[],
                dl_speed=0,
                ul_speed=0,
                active_torrents=0,
                progress=0.0,
                eta=0
            )
