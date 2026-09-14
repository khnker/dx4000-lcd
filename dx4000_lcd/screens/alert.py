from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.tokens import DiskToken, StateToken, TemperatureToken


class AlertScreen:
    def render(self, alert) -> ScreenOutput:
        source = getattr(alert, "source", "") or ""
        health = getattr(alert, "health", None)

        source_str = DiskToken.render(source).upper().strip()

        if health is not None:
            health_val = getattr(health, "value", None) or str(health)
            health_str = StateToken.render(str(health_val)).strip()
            line1 = f"! {source_str} {health_str}"
        else:
            line1 = f"! {source_str}"

        temp = getattr(alert, "temp_c", None)
        if temp is not None:
            temp_str = TemperatureToken.render(temp).strip()
            message = f"{source_str} {temp_str}"
        else:
            message = getattr(alert, "message", "") or ""

        return ScreenOutput(
            line1=fit_line(line1),
            line2=fit_line(message[:16]),
        )
