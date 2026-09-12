import time
from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.screens.status import StatusScreen
from dx4000_lcd.screens.storage import StorageScreen
from dx4000_lcd.screens.system import SystemScreen
from dx4000_lcd.screens.network import NetworkScreen
from dx4000_lcd.screens.torrent import TorrentScreen
from dx4000_lcd.screens.alert import AlertScreen

class ScreenManager:
    _screens = None
    SCREEN_TIMES = {
        "status": 4,
        "storage": 3,
        "torrent": 5,
        "system": 3,
        "network": 3,
    }

    def __init__(self):
        if ScreenManager._screens is None:
            ScreenManager._screens = {
                "status": StatusScreen(),
                "storage": StorageScreen(),
                "system": SystemScreen(),
                "network": NetworkScreen(),
                "torrent": TorrentScreen(),
            }
        self._index = 0
        self._manual_until = 0
        self._alert_until = 0
        self._screen_names = list(self._screens.keys())

    @property
    def current_screen_name(self) -> str:
        return self._screen_names[self._index]

    def render(self, state, health_results=None) -> ScreenOutput:
        # Check for alerts with expiration
        if health_results:
            for hr in health_results:
                if hr.health.value in ("error", "warn"):
                    if time.monotonic() < self._alert_until:
                        return AlertScreen().render(hr)
                    else:
                        self._alert_until = time.monotonic() + 5
                        return AlertScreen().render(hr)
        
        return self._screens[self.current_screen_name].render(state)

    def next(self):
        self._index = (self._index + 1) % len(self._screen_names)
        self._manual_until = time.monotonic() + 15

    def previous(self):
        self._index = (self._index - 1) % len(self._screen_names)
        self._manual_until = time.monotonic() + 15
