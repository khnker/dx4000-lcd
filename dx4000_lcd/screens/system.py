from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp


def _val(obj):
    if obj is None:
        return None
    if hasattr(obj, "value"):
        return obj.value
    return obj


class SystemScreen:
    def render(self, state) -> ScreenOutput:
        cpu = getattr(state, "cpu", None)

        usage_raw = None
        if cpu is not None:
            usage_raw = _val(getattr(cpu, "usage_pct", None))
            if usage_raw is None:
                usage_raw = _val(getattr(cpu, "usage", None))
        usage = int(usage_raw) if usage_raw is not None else 0

        temp_raw = None
        if cpu is not None:
            temp_raw = getattr(cpu, "temp_c", None)
            if temp_raw is None:
                temp_raw = getattr(cpu, "temp", None)
        temp = format_temp(_val(temp_raw))

        memory = getattr(state, "memory", None)
        ram_raw = _val(getattr(memory, "used_pct", None) if memory is not None else None)
        ram_pct = round(ram_raw) if ram_raw is not None else 0

        load_raw = None
        if cpu is not None:
            load_raw = getattr(cpu, "load_1m", None)
            if load_raw is None:
                load_raw = getattr(cpu, "load1", None)
            if load_raw is None:
                load_raw = getattr(cpu, "load", None)
        if load_raw is None:
            load_raw = getattr(state, "load", None)
        load_val = _val(load_raw)
        load = float(load_val) if load_val is not None else 0.0

        return ScreenOutput(
            line1=fit_line(f"CPU {usage}% {temp}"),
            line2=fit_line(f"RAM {ram_pct}% L{load:.2f}"),
        )
