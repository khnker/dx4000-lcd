import time
from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.screens.status import StatusScreen
from dx4000_lcd.screens.storage import StorageScreen
from dx4000_lcd.screens.system import SystemScreen
from dx4000_lcd.screens.network import NetworkScreen
from dx4000_lcd.screens.torrent import TorrentScreen
from dx4000_lcd.screens.disk import DiskScreen
from dx4000_lcd.screens.alert import AlertScreen
from dx4000_lcd.health import highest_priority_alert

class ScreenManager:
    SCREENS = ["status", "storage", "disk", "system", "network", "torrent"]
    SCREEN_TIMES = {
        "status": 4,
        "storage": 3,
        "disk": 3,
        "torrent": 5,
        "system": 3,
        "network": 3,
    }

    def __init__(self):
        self.index = 0
        self.manual_until = 0
        self.torrent_index = 0
        self.torrent_cycle = 0
        self.screens = {
            "status": StatusScreen(),
            "storage": StorageScreen(),
            "disk": DiskScreen(),
            "system": SystemScreen(),
            "network": NetworkScreen(),
            "torrent": TorrentScreen(),
        }

    def render(self, state, health_results=None) -> ScreenOutput:
        if health_results:
            top_alert = highest_priority_alert(health_results)
            if top_alert and top_alert.health.value in ("error", "warn"):
                return AlertScreen().render(top_alert)

        screen_name = self.SCREENS[self.index]
        
        if screen_name == "torrent":
            self.torrent_cycle += 1
            if self.torrent_cycle >= 3:
                self.torrent_cycle = 0
                if state.torrent and state.torrent.torrent_names:
                    self.torrent_index = (self.torrent_index + 1) % len(state.torrent.torrent_names)
            screen = self.screens.get(screen_name)
            return screen.render(state, self.torrent_index)

        screen = self.screens.get(screen_name, self.screens["status"])
        return screen.render(state)

    def next(self):
        self.index = (self.index + 1) % len(self.SCREENS)
        self.manual_until = time.monotonic() + 15

    def previous(self):
        self.index = (self.index - 1) % len(self.SCREENS)
        self.manual_until = time.monotonic() + 15

    def current_screen_name(self) -> str:
        return self.SCREENS[self.index]
    
    def current_duration(self) -> int:
        return self.SCREEN_TIMES.get(self.SCREENS[self.index], 3)
