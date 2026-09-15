from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.tokens import TemperatureToken
from dx4000_lcd.layouts import layout_alert


class AlertScreen:
    def render(self, alert) -> ScreenOutput:
        source = getattr(alert, "source", "") or ""
        health = getattr(alert, "health", None)
        message = getattr(alert, "message", "") or ""

        if health is not None and hasattr(health, "value"):
            health_str = str(health.value).upper()
        elif health is not None:
            health_str = str(health).upper()
        else:
            health_str = ""

        temp_c = getattr(alert, "temp_c", None)
        temp_str = TemperatureToken.render(temp_c) if temp_c is not None else ""

        # For disk alerts, show the specific issue
        if "UNCORRECTABLE" in message:
            line1 = f"! {source.upper()} ERR"
            line2 = "UNCORRECTABLE"
        elif "TIMEOUTS" in message:
            line1 = f"! {source.upper()} WARN"
            line2 = "TIMEOUTS"
        elif "REALLOCATED" in message:
            line1 = f"! {source.upper()} WARN"
            line2 = "REALLOCATED"
        elif "HOT" in message:
            line1 = f"! {source.upper()} HOT"
            line2 = f"{temp_str} CRITICAL"
        elif "WARM" in message:
            line1 = f"! {source.upper()} WARM"
            line2 = f"{temp_str} HIGH"
        else:
            line1, line2 = layout_alert(source, message, temp_str)

        return ScreenOutput(
            line1=fit_line(line1[:16]),
            line2=fit_line(line2[:16]),
        )