from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.tokens import TemperatureToken, FanToken, PercentToken
from dx4000_lcd.health import get_hottest_disk
from dx4000_lcd.layouts import layout_status


def _val(obj):
    if obj is None:
        return None
    if hasattr(obj, "value"):
        return obj.value
    return obj


class StatusScreen:
    def render(self, state) -> ScreenOutput:
        cpu = getattr(state, "cpu", None)
        cpu_temp = _val(getattr(cpu, "temp_c", None)) if cpu else None
        cpu_temp_str = TemperatureToken.render(cpu_temp)

        hottest = get_hottest_disk(state)
        disk_temp = _val(hottest.temp_c) if hottest else None
        disk_temp_str = TemperatureToken.render(disk_temp)

        fan = getattr(state, "fan", None)
        fan_rpm = _val(getattr(fan, "rpm", None)) if fan else None
        fan_str = FanToken.render(fan_rpm)

        storage = getattr(state, "storage", None)
        storage_pct = _val(getattr(storage, "used_pct", None)) if storage else None
        storage_str = PercentToken.render(storage_pct)

        line1, line2 = layout_status(cpu_temp_str, fan_str, disk_temp_str, storage_str)

        return ScreenOutput(
            line1=fit_line(line1),
            line2=fit_line(line2),
        )
