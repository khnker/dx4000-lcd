from dx4000_lcd.state import SystemState


def render_line(text: str) -> str:
    return text[:16].ljust(16).replace(" ", "\\ ")


class HealthEngine:
    @staticmethod
    def calculate(state: SystemState) -> str:
        if state.cpu.temp_c and state.cpu.temp_c >= 60:
            return "HOT"
        for d in state.disks:
            if d.temp_c and d.temp_c >= 45:
                return "HOT"
        return "OK"


def build_screens(state: SystemState):
    disk_temps = {d.name: d.temp_c for d in state.disks if d.temp_c is not None}
    disk_max = max(disk_temps.values()) if disk_temps else 0
    status = HealthEngine.calculate(state)

    screens = []

    # Pantalla 1: HOME
    screens.append((
        render_line(f"NAS {status} {state.cpu.temp_c or 0:.0f}C"),
        render_line(f"DSK {disk_max:.0f}C {state.torrent.active_torrents}T")
    ))

    # Pantalla 2: STORAGE (mergerfs pool)
    total_tb = state.storage.total_bytes / (1024 ** 4)
    used_tb = state.storage.used_bytes / (1024 ** 4)
    pct = state.storage.used_pct
    screens.append((
        render_line(f"POOL {used_tb:.1f}/{total_tb:.1f}T"),
        render_line(f"FREE {pct:.0f}% USED")
    ))

    # Pantalla 3: TORRENT
    dl_mb = state.torrent.dl_speed / (1024 * 1024)
    ul_mb = state.torrent.ul_speed / (1024 * 1024)
    screens.append((
        render_line(f"TOR {state.torrent.active_torrents} ACTIVE"),
        render_line(f"DL {dl_mb:.1f}M UP{ul_mb:.1f}M")
    ))

    return screens
