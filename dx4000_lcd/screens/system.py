from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line

class SystemScreen:
    def render(self, state) -> ScreenOutput:
        temp = state.cpu.temp_c if state.cpu.temp_c else 0
        return ScreenOutput(
            line1=fit_line(f"CPU {temp}C"),
            line2=fit_line(f"LOAD {state.cpu.load_1m:.2f}"),
        )
