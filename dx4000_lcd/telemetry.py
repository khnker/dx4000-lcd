from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class TelemetryValue:
    value: Any = None
    timestamp: float = 0.0
    status: str = "UNKNOWN" # VALID, UNKNOWN, STALE, ERROR

    @property
    def value_or_default(self):
        return self.value
