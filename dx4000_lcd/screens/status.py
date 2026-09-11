from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp
from dx4000_lcd.bar import render_bar
from dx4000_lcd.health import HealthEngine, highest_priority_alert
from dx4000_lcd.screens.alert import AlertScreen


class StatusScreen:
    def __init__(self):
        self.health_engine = HealthEngine()

    def render(self, state) -> ScreenOutput:
        results = self.health_engine.evaluate(state)
        alert = highest_priority_alert(results)
        if alert:
            return AlertScreen().render(alert)

        cpu = format_temp(state.cpu.temp_c)
        disk_temps = [d.temp_c for d in state.disks if d.temp_c is not None]
        disk = format_temp(max(disk_temps)) if disk_temps else "--C"

        bar = render_bar(state.storage.used_pct, 7)
        pct = round(state.storage.used_pct)

        return ScreenOutput(
            line1=fit_line(f"NAS OK {cpu} {disk}"),
            line2=fit_line(f"STO {bar} {pct}%"),
        )
