import urllib.request
import urllib.parse
import json
from dx4000_lcd.state import TorrentState, SystemState


class TorrentCollector:
    def __init__(self, host="127.0.0.1", port=8080, user="admin", passwd="adminadmin"):
        self.url_base = f"http://{host}:{port}"
        self.user = user
        self.passwd = passwd
        self.cookie = None

    def login(self):
        try:
            data = urllib.parse.urlencode({"username": self.user, "password": self.passwd}).encode("utf-8")
            req = urllib.request.Request(f"{self.url_base}/api/v2/auth/login", data=data)
            resp = urllib.request.urlopen(req, timeout=2)
            headers = resp.headers.get_all("Set-Cookie")
            if headers:
                for h in headers:
                    if "SID=" in h:
                        self.cookie = h.split(";")[0]
                        return True
        except Exception:
            pass
        return False

    def read(self, state: SystemState):
        if not self.cookie:
            self.login()
        try:
            req = urllib.request.Request(f"{self.url_base}/api/v2/torrents/info")
            if self.cookie:
                req.add_header("Cookie", self.cookie)
            resp = urllib.request.urlopen(req, timeout=2)
            torrents = json.loads(resp.read().decode())

            active = sum(1 for t in torrents if t.get("dlspeed", 0) > 0 or t.get("upspeed", 0) > 0)
            dl = sum(t.get("dlspeed", 0) for t in torrents)
            ul = sum(t.get("upspeed", 0) for t in torrents)

            state.torrent = TorrentState(dl_speed=dl, ul_speed=ul, active_torrents=active)
        except Exception:
            if self.login():
                self.read(state)
            else:
                state.torrent = TorrentState()
