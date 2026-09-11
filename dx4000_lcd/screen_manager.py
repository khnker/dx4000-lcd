import time
from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.screens.status import StatusScreen
from dx4000_lcd.screens.storage import StorageScreen
from dx4000_lcd.screens.system import SystemScreen
from dx4000_lcd.screens.network import NetworkScreen
from dx4000_lcd.screens.torrent import TorrentScreen
from dx4000_lcd.screens.alert import AlertScreen

class ScreenManager:
    SCREENS = ("status", "storage", "torrent", "system", "network")

    def __init__(self):
        self.index = 0
        self.manual_until = 0

    def render(self, state, health_results=None) -> ScreenOutput:
        # Prioritize alerts over normal rotation
        if health_results:
            for hr in health_results:
                if hr.health.value in ("error", "warn"):
                    return AlertScreen().render(hr)
        
        # Normal rotation
        screen_name = self.SCREENS[self.index]
        if screen_name == "status":
            return StatusScreen().render(state)
        elif screen_name == "storage":
            return StorageScreen().render(state)
        elif screen_name == "system":
            return SystemScreen().render(state)
        elif screen_name == "network":
            return NetworkScreen().render(state)
        elif screen_name == "torrent":
            return TorrentScreen().render(state)
        return StatusScreen().render(state)

    def next(self):
        self.index = (self.index + 1) % len(self.SCREENS)
        self.manual_until = time.monotonic() + 15

    def previous(self):
        self.index = (self.index - 1) % len(self.SCREENS)
        self.manual_until = time.monotonic() + 15
