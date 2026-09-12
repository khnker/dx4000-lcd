from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

def format_temp(value):
    if value is None:
        return "--"
    return f"{value:02d}C"

def format_pct(value):
    if value is None:
        return "--"
    return f"{int(value)}%"

class SystemScreen:
    def render(self, state) -> ScreenOutput:
        cpu_usage = format_pct(state.cpu.usage_pct)
        cpu_temp = format_temp(state.cpu.temp_c)
        ram_pct = "--"
        
        if hasattr(state, 'memory') and state.memory.used_pct:
            ram_pct = format_pct(state.memory.used_pct)
        
        load = f"{state.cpu.load_1m:.2f}" if state.cpu.load_1m else "--"
        
        return ScreenOutput(
            line1=fit_line(f"CPU {cpu_usage} {cpu_temp}"),
            line2=fit_line(f"RAM {ram_pct} L{load}"),
        )
