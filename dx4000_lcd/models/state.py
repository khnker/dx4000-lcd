from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class CpuStatus:
    temp_c: int = 0
    load_1m: float = 0.0


@dataclass
class FanStatus:
    pwm: int = 0
    rpm: int = 0


@dataclass
class DiskHealth:
    device: str = ""
    temperature_c: Optional[int] = None
    smart_ok: bool = True


@dataclass
class StorageStatus:
    mountpoint: str = "/"
    total_bytes: int = 0
    used_bytes: int = 0
    free_bytes: int = 0
    percent_used: float = 0.0
    mergerfs: bool = False


@dataclass
class NetworkStatus:
    ip: str = "0.0.0.0"
    rx_bps: int = 0
    tx_bps: int = 0


@dataclass
class NasState:
    cpu: CpuStatus = field(default_factory=CpuStatus)
    fan: FanStatus = field(default_factory=FanStatus)
    storage: StorageStatus = field(default_factory=StorageStatus)
    disks: List[DiskHealth] = field(default_factory=list)
    network: NetworkStatus = field(default_factory=NetworkStatus)
    status: str = "OK"
