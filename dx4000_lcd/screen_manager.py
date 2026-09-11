import time
from typing import List

from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.screens.status import StatusScreen
from dx4000_lcd.screens.storage import StorageScreen
from dx4000_lcd.screens.system import SystemScreen
from dx4000_lcd.screens.network import NetworkScreen
from dx4000_lcd.screens.torrent import TorrentScreen
from dx4000_lcd.screens.disks import DiskScreen


class ScreenManager:
    NORMAL_SCREENS = ("status", "storage", "torrent", "system", "network")

    def __init__(self):
        self.index = 0
        self.manual_until = 0

    @property
    def current_screen_name(self) -> str:
        return self.NORMAL_SCREENS[self.index]

    def next(self):
        self.index = (self.index + 1) % len(self.NORMAL_SCREENS)
        self.manual_until = time.monotonic() + 15

    def previous(self):
        self.index = (self.index - 1) % len(self.NORMAL_SCREENS)
        self.manual_until = time.monotonic() + 15

    def get_screen(self, state) -> ScreenOutput:
        name = self.current_screen_name
        if name == "status":
            return StatusScreen().render(state)
        elif name == "storage":
            return StorageScreen().render(state)
        elif name == "system":
            return SystemScreen().render(state)
        elif name == "network":
            return NetworkScreen().render(state)
        elif name == "torrent":
            return TorrentScreen().render(state)
        return StatusScreen().render(state)