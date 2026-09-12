from dataclasses import dataclass, field
from typing import Optional, List


from dx4000_lcd.telemetry import TelemetryValue

@dataclass
class CpuState:
    usage_pct: TelemetryValue = field(default_factory=TelemetryValue)
    temp_c: TelemetryValue = field(default_factory=TelemetryValue)
    load_1m: TelemetryValue = field(default_factory=TelemetryValue)



@dataclass
class MemoryState:
    used_pct: float = 0.0
    available_mb: float = 0.0
    total_mb: float = 0.0


@dataclass
class FanState:
    rpm: int = 0
    pwm: Optional[int] = None


@dataclass
class DiskState:
    name: str = ""
    temp_c: Optional[int] = None
    health: str = "UNKNOWN"


@dataclass
class StorageState:
    mountpoint: str = "/"
    total_bytes: int = 0
    used_bytes: int = 0
    free_bytes: int = 0
    mergerfs: bool = False

    @property
    def used_pct(self) -> float:
        if self.total_bytes == 0:
            return 0.0
        return (self.used_bytes / self.total_bytes) * 100.0


@dataclass
class NetworkState:
    ip: str = ""
    rx_bps: int = 0
    tx_bps: int = 0


@dataclass
class TorrentState:
    dl_speed: int = 0
    ul_speed: int = 0
    active_torrents: int = 0
    torrent_name: str = ""
    progress: float = 0.0
    eta: int = 0


@dataclass
class SystemState:
    cpu: CpuState = field(default_factory=CpuState)
    memory: MemoryState = field(default_factory=MemoryState)
    fan: FanState = field(default_factory=FanState)
    disks: List[DiskState] = field(default_factory=list)
    storage: StorageState = field(default_factory=StorageState)
    network: NetworkState = field(default_factory=NetworkState)
    torrent: TorrentState = field(default_factory=TorrentState)
    uptime_seconds: int = 0
    status: str = "OK"
