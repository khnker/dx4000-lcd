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
        
        cpu_temp = state.cpu.temp_c.value if hasattr(state.cpu.temp_c, "value") else state.cpu.temp_c
        if cpu_temp is None:
            results.append(HealthResult(Health.UNKNOWN, "cpu", "CPU TEMP?"))
        elif cpu_temp >= 80:
            results.append(HealthResult(Health.ERROR, "cpu", "CPU HOT"))
        elif cpu_temp >= 70:
            results.append(HealthResult(Health.WARN, "cpu", "CPU WARM"))
        
        for disk in getattr(state, "disks", []) or []:
            if disk.temp_c is None:
                continue
            if disk.temp_c >= 50:
                results.append(HealthResult(Health.ERROR, "disk", f"{disk.name} HOT"))
            elif disk.temp_c >= 45:
                results.append(HealthResult(Health.WARN, "disk", f"{disk.name} WARM"))
        
        fan = getattr(state, "fan", None)
        if fan:
            if fan.rpm == 0 or fan.rpm is None:
                if getattr(fan, "status", "") == "ERROR":
                    results.append(HealthResult(Health.ERROR, "fan", "FAN ERROR"))
        
        storage = getattr(state, "storage", None)
        if storage:
            used_pct = storage.used_pct
            if used_pct >= 95:
                results.append(HealthResult(Health.ERROR, "storage", "STORAGE FULL"))
            elif used_pct >= 85:
                results.append(HealthResult(Health.WARN, "storage", "STORAGE HIGH"))
        
        return results

def get_hottest_disk(state) -> any:
    disks = getattr(state, "disks", []) or []
    valid = [d for d in disks if d.temp_c is not None]
    if not valid:
        return None
    return max(valid, key=lambda d: d.temp_c)

def highest_priority_alert(results: list[HealthResult]) -> HealthResult | None:
    priority = {Health.ERROR: 3, Health.WARN: 2, Health.UNKNOWN: 1, Health.OK: 0}
    active = [r for r in results if r.health != Health.OK]
    if not active:
        return None
    return max(active, key=lambda r: priority[r.health])
