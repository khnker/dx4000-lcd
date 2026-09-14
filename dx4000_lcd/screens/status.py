from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp


def _val(obj):
    if obj is None:
        return None
    if hasattr(obj, "value"):
        return obj.value
    return obj


class StatusScreen:
    def render(self, state) -> ScreenOutput:
        cpu = getattr(state, "cpu", None)
        cpu_temp_raw = None
        if cpu is not None:
            cpu_temp_raw = getattr(cpu, "temp_c", None)
            if cpu_temp_raw is None:
                cpu_temp_raw = getattr(cpu, "temp", None)
        cpu_temp = format_temp(_val(cpu_temp_raw))

        disks = getattr(state, "disks", None) or []
        if disks:
            hottest = max(
                disks,
                key=lambda d: d.temp_c if getattr(d, "temp_c", None) is not None else -1,
            )
            disk_temp = format_temp(_val(hottest.temp_c))
        else:
            disk_temp = format_temp(None)

        fan = getattr(state, "fan", None)
        rpm = None
        if fan is not None:
            rpm = _val(getattr(fan, "rpm", None))
            if rpm is None:
                rpm = _val(getattr(fan, "rpm_fan1", None))
        if rpm is None or rpm == 0:
            fan_text = "--"
        elif rpm >= 1000:
            fan_text = f"{int(rpm) // 1000}K"
        else:
            fan_text = str(int(rpm))

        storage = getattr(state, "storage", None)
        used_pct = _val(getattr(storage, "used_pct", None) if storage is not None else None)
        pct_text = "--" if used_pct is None else str(round(used_pct))

        return ScreenOutput(
            line1=fit_line(f"CPU {cpu_temp} FAN {fan_text}"),
            line2=fit_line(f"DSK {disk_temp} STO {pct_text}%"),
        )
