import urllib.request
import urllib.parse
import json
import http.cookiejar
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class TorrentState:
    name: str
    state: str
    progress: float
    downloaded: int
    total: int
    ratio: float
    peers: int


def fetch_torrents(host: str = "10.10.10.101", port: int = 8080,
                   username: str = "admin", password: str = "admin") -> Optional[List[TorrentState]]:
    """Obtiene el estado de los torrents desde qBittorrent WebUI."""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    base = f"http://{host}:{port}"

    # Login
    login_data = urllib.parse.urlencode({
        "username": username,
        "password": password
    }).encode()

    try:
        opener.open(f"{base}/api/v2/auth/login", login_data)
    except Exception as e:
        print(f"Login failed: {e}")
        return None

    # Get torrents info
    try:
        response = opener.open(f"{base}/api/v2/torrents/info", timeout=5)
        data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Fetch failed: {e}")
        return None

    torrents = []
    for t in data:
        torrents.append(TorrentState(
            name=t.get("name", ""),
            state=t.get("state", ""),
            progress=t.get("progress", 0.0),
            downloaded=t.get("downloaded", 0),
            total=t.get("total", 0),
            ratio=t.get("ratio", 0.0),
            peers=t.get("num_peers", 0)
        ))
    return torrents