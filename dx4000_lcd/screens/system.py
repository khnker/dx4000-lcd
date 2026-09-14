from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_temp

class SystemScreen:
    def render(self, state) -> ScreenOutput:
        cpu = state.cpu

        usage_val = cpu.usage_pct.value if hasattr(cpu.usage_pct, "value") and cpu.usage_pct.value is not None else (cpu.usage_pct if isinstance(cpu.usage_pct, (int, float)) else 0)
        temp_val = cpu.temp_c.value if hasattr(cpu.temp_c, "value") and cpu.temp_c.value is not None else (cpu.temp_c if isinstance(cpu.temp_c, (int, float)) else 0)
        load_val = cpu.load_1m.value if hasattr(cpu.load_1m, "value") and cpu.load_1m.value is not None else (cpu.load_1m if isinstance(cpu.load_1m, (int, float)) else 0)

        line1 = fit_line(f"CPU {usage_val}% {format_temp(temp_val)}")
        line2 = fit_line(f"RAM {state.memory.used_pct:.0f}% L{load_val:.2f}")

        return ScreenOutput(line1=line1, line2=line2)
