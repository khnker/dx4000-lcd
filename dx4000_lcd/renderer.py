from dx4000_lcd.state import NasState, DiskHealth


def render_line(text: str) -> str:
    return text[:16].ljust(16)


class HealthEngine:
    @staticmethod
    def calculate(state: NasState) -> str:
        if state.cpu.temp_c and state.cpu.temp_c >= 60:
            return "HOT"
        for d in state.disks:
            if d.temperature_c and d.temperature_c >= 45:
                return "HOT"
        return "OK"


def build_screens(state: NasState) -> list:
    disk_temps = [(d.device, d.temperature_c) for d in state.disks if d.temperature_c is not None]
    disk_max = max((t or 0 for _, t in disk_temps), default=0)
    status = HealthEngine.calculate(state)

    screens = [
        (render_line(f"CPU {state.cpu.temp_c or 0:>3}C {status}"),
         render_line(f"DSK {disk_max:>3}C P{state.fan.pwm or 0:>3}")),
    ]
    return screens