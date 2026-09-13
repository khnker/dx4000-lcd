from enum import Enum
from dataclasses import dataclass

class Health(Enum):
    OK = "ok"
    WARN = "warn"
    ERROR = "error"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class HealthResult:
    health: Health
    source: str
    message: str

class HealthEngine:
    def evaluate(self, state) -> list[HealthResult]:
        results = []
        temp = state.cpu.temp_c
        temp_val = temp.value if hasattr(temp, "value") else temp
        
        if temp_val is None:
            results.append(HealthResult(Health.UNKNOWN, "cpu", "CPU TEMP?"))
        elif temp_val >= 80:
            results.append(HealthResult(Health.ERROR, "cpu", "CPU HOT"))
        elif temp_val >= 70:
            results.append(HealthResult(Health.WARN, "cpu", "CPU WARM"))
        return results

def highest_priority_alert(results: list[HealthResult]) -> HealthResult | None:
    priority = {Health.ERROR: 3, Health.WARN: 2, Health.UNKNOWN: 1, Health.OK: 0}
    active = [r for r in results if r.health != Health.OK]
    if not active:
        return None
    return max(active, key=lambda r: priority[r.health])
