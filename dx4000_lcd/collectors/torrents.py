from dx4000_lcd.state import SystemState
from dx4000_lcd.collectors import CpuCollector, DiskTempCollector, FanCollector, StorageCollector
from dx4000_lcd.torrents import TorrentCollector

class TorrentCollectorWrapper:
    def __init__(self):
        self.tc = TorrentCollector()
    def read(self, state: SystemState):
        self.tc.read(state)
        state.torrent_dl = state.torrent_dl or 0
        state.torrent_ul = state.torrent_ul or 0
