from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.tokens import PercentToken, TemperatureToken, LoadToken


def _val(obj):
    if obj is None:
        return None
    if hasattr(obj, "value"):
        return obj.value
    return obj


class SystemScreen:
    def render(self, state) -> ScreenOutput:
        cpu = getattr(state, "cpu", None)
        usage = _val(getattr(cpu, "usage_pct", None)) if cpu else None
        temp = _val(getattr(cpu, "temp_c", None)) if cpu else None
        load = _val(getattr(cpu, "load_1m", None)) if cpu else None

        memory = getattr(state, "memory", None)
        ram_pct = _val(getattr(memory, "used_pct", None)) if memory else None

        return ScreenOutput(
            line1=fit_line(f"CPU {PercentToken.render(usage)} {TemperatureToken.render(temp)}"),
            line2=fit_line(f"RAM {PercentToken.render(ram_pct)} {LoadToken.render(load)}"),
        )