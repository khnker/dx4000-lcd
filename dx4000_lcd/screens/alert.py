from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line


class AlertScreen:
    def render(self, alert) -> ScreenOutput:
        if hasattr(alert, "alert") and not hasattr(alert, "source"):
            alert = alert.alert

        source = getattr(alert, "source", "") or ""
        health = getattr(alert, "health", None)
        if health is not None and hasattr(health, "value"):
            health_str = str(health.value).upper()
        elif health is not None:
            health_str = str(health).upper()
        else:
            health_str = ""

        message = getattr(alert, "message", "") or ""
        line1 = f"! {source.upper()} {health_str}".strip()
        return ScreenOutput(
            line1=fit_line(line1),
            line2=fit_line(message[:16]),
        )
