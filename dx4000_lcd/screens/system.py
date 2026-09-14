from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp, format_bytes
from dx4000_lcd.icons import TEMP

class SystemScreen:
    def render(self, state) -> ScreenOutput:
        cpu = state.cpu

        usage_val = cpu.usage_pct.value if hasattr(cpu.usage_pct, "value") and cpu.usage_pct.value is not None else (cpu.usage_pct if isinstance(cpu.usage_pct, (int, float)) else 0)
        temp_val = cpu.temp_c.value if hasattr(cpu.temp_c, "value") and cpu.temp_c.value is not None else (cpu.temp_c if isinstance(cpu.temp_c, (int, float)) else 0)
        load_val = cpu.load_1m.value if hasattr(cpu.load_1m, "value") and cpu.load_1m.value is not None else (cpu.load_1m if isinstance(cpu.load_1m, (int, float)) else 0)

        line1 = (
            f"CPU {usage_val}% "
            f"{TEMP}{format_temp(temp_val)} "
            f"L{load_val:.2f}"
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