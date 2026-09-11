from dx4000_lcd.state import SystemState


def render_line(text: str) -> str:
    escaped = text.replace(" ", "\\ ")
    return escaped[:16]


import time


class ScrollText:
    def __init__(self, speed=2):
        self.pos = 0
        self.text = ""
        self.speed = speed
        self.last_tick = 0.0

    def update(self, text: str) -> str:
        if text != self.text:
            self.text = text
            self.pos = 0
            self.last_tick = time.time()
        if len(text) <= 16:
            return text
        now = time.time()
        if now - self.last_tick >= self.speed:
            self.pos = (self.pos + 1) % len(text)
            self.last_tick = now
        visible = text[self.pos:self.pos + 16]
        if len(visible) < 16:
            visible += text[:16 - len(visible)]
        return visible


class HealthEngine:
    @staticmethod
    def calculate(state: SystemState) -> str:
        if state.cpu.temp_c and state.cpu.temp_c >= 60:
            return "HOT"
        for d in state.disks:
            if d.temp_c and d.temp_c >= 45:
                return "HOT"
        return "OK"


def build_screens(state: SystemState, scroll: ScrollText):
    disk_temps = {d.name: d.temp_c for d in state.disks if d.temp_c is not None}
    disk_max = max(disk_temps.values()) if disk_temps else 0
    status = HealthEngine.calculate(state)

    screens = []

    screens.append((
        render_line(f"NAS {status} {state.cpu.temp_c or 0:.0f}C"),
        render_line(f"DSK {disk_max:.0f}C {state.torrent.active_torrents}T")
    ))

    total_tb = state.storage.total_bytes / (1024 ** 4)
    used_tb = state.storage.used_bytes / (1024 ** 4)
    pct = state.storage.used_pct
    screens.append((
        render_line(f"POOL {used_tb:.1f}/{total_tb:.1f}T"),
        render_line(f"FREE {pct:.0f}% USED")
    ))

    dl_mb = state.torrent.dl_speed / (1024 * 1024)
    ul_mb = state.torrent.ul_speed / (1024 * 1024)
    if state.torrent.torrent_name:
        scrolled = scroll.update(state.torrent.torrent_name)
        screens.append((
            render_line(scrolled),
            render_line(f"{state.torrent.progress:.0f}% DL{dl_mb:.1f}M")
        ))
    else:
        screens.append((
            render_line(f"TOR {state.torrent.active_torrents} IDLE"),
            render_line(f"DL {dl_mb:.1f}M UP{ul_mb:.1f}M")
        ))

    return screens
