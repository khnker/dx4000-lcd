from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp, format_bytes

class SystemScreen:
    def render(self, state) -> ScreenOutput:
        cpu = state.cpu
        
        line1 = (
            f"CPU {cpu.usage_pct.value if cpu.usage_pct.value is not None else 0}% "
            f"{format_temp(cpu.temp_c.value)} "
            f"L{cpu.load_1m.value if cpu.load_1m.value is not None else 0:.2f}"
        )
        
        used_mb = state.memory.total_mb - state.memory.available_mb
        
        line2 = (
            f"RAM {state.memory.used_pct:.0f}% "
            f"{format_bytes(int(used_mb * 1024 * 1024))}/"
            f"{format_bytes(int(state.memory.total_mb * 1024 * 1024))}"
        )
        
        return ScreenOutput(
            line1=fit_line(line1),
            line2=fit_line(line2),
        )
