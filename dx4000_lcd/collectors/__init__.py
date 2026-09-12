# Collectors - import from individual modules
from dx4000_lcd.collectors.cpu import CpuCollector
from dx4000_lcd.collectors.memory import MemoryCollector
from dx4000_lcd.collectors.fan import FanCollector
from dx4000_lcd.collectors.disk_smart import DiskSmartCollector as DiskCollector
from dx4000_lcd.collectors.storage import StorageCollector
from dx4000_lcd.collectors.network import NetworkCollector
from dx4000_lcd.collectors.torrents import TorrentCollector
from dx4000_lcd.collectors.uptime import UptimeCollector

__all__ = [
    "CpuCollector",
    "MemoryCollector",
    "FanCollector",
    "DiskCollector",
    "StorageCollector",
    "NetworkCollector",
    "TorrentCollector",
    "UptimeCollector",
]
