from dataclasses import dataclass
from typing import Optional, List

@dataclass
class TorrentState:
    name: str
    status: str  # "downloading", "seeding", "paused", "error"
    progress: float
    downloaded: int
    total: int
    ratio: float
    peers: int
