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
        
        # CPU Temp
        if state.cpu.temp_c is None:
            results.append(HealthResult(Health.UNKNOWN, "cpu", "CPU TEMP?"))
        elif state.cpu.temp_c >= 80:
            results.append(HealthResult(Health.ERROR, "cpu", "CPU HOT"))
        elif state.cpu.temp_c >= 70:
            results.append(HealthResult(Health.WARN, "cpu", "CPU WARM"))
            
        # Disks Temp
        for d in state.disks:
            if d.temp_c is None:
                results.append(HealthResult(Health.UNKNOWN, d.name, "SMART?"))
            elif d.temp_c >= 50:
                results.append(HealthResult(Health.ERROR, d.name, f"{d.name} HOT"))
            elif d.temp_c >= 45:
                results.append(HealthResult(Health.WARN, d.name, f"{d.name} WARM"))
                
        return results

def highest_priority_alert(results: list[HealthResult]) -> HealthResult | None:
    priority = {
        Health.ERROR: 3,
        Health.WARN: 2,
        Health.UNKNOWN: 1,
        Health.OK: 0,
    }
    active = [r for r in results if r.health != Health.OK]
    if not active:
        return None
    return max(active, key=lambda r: priority[r.health])
