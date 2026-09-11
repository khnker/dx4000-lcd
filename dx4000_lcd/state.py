from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class DiskState:
    name: str
    temp_c: Optional[float] = None
    health: str = "UNKNOWN"

@dataclass
class CpuState:
    usage_pct: float = 0.0
    temp_c: Optional[float] = None
    load_1m: float = 0.0

@dataclass
class SystemState:
    cpu: CpuState = field(default_factory=CpuState)
    disks: List[DiskState] = field(default_factory=list)
    status: str = "OK"
