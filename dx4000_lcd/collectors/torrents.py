import urllib.request
import urllib.parse
import json
from http.cookiejar import CookieJar
from dx4000_lcd.state import TorrentState, SystemState


class TorrentCollector:
    def __init__(self, host="127.0.0.1", port=8080, user="admin", passwd="adminadmin"):
        self.url_base = f"http://{host}:{port}/api/v2"
        self.user = user
        self.passwd = passwd
        self.cj = CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self.logged_in = False

    def login(self):
        try:
            data = urllib.parse.urlencode({"username": self.user, "password": self.passwd}).encode()
            self.opener.open(f"{self.url_base}/auth/login", data=data)
            self.logged_in = True
        except:
            self.logged_in = False

    def _fetch(self):
        resp = self.opener.open(f"{self.url_base}/torrents/info", timeout=5)
        return json.loads(resp.read().decode())

    def read(self, state: SystemState):
        try:
            if not self.logged_in:
                self.login()
            torrents = self._fetch()

            dl = sum(t.get("dlspeed", 0) for t in torrents)
            ul = sum(t.get("upspeed", 0) for t in torrents)
            downloading = [t for t in torrents if t.get("dlspeed", 0) > 0]
            active = len(downloading)

            name = ""
            progress = 0.0
            eta = 0
            if downloading:
                t = downloading[0]
                name = t.get("name", "")
                progress = t.get("progress", 0.0) * 100
                eta = t.get("eta", 0)
            elif torrents:
                for t in torrents:
                    if t.get("progress", 1.0) < 1.0:
                        name = t.get("name", "")
                        progress = t.get("progress", 0.0) * 100
                        eta = t.get("eta", 0)
                        break

            state.torrent = TorrentState(
                dl_speed=dl,
                ul_speed=ul,
                active_torrents=active,
                torrent_name=name,
                progress=progress,
                eta=eta,
            )
        except Exception:
            state.torrent = TorrentState()
