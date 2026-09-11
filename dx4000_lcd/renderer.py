from dx4000_lcd.state import SystemState


def render_line(text: str) -> str:
    visible = text[:16]
    return visible.replace(" ", "\\ ")


class HealthEngine:
    @staticmethod
    def calculate(state: SystemState) -> str:
        if state.cpu.temp_c and state.cpu.temp_c >= 60:
            return "WARN"
        for d in state.disks:
            if d.temp_c and d.temp_c >= 45:
                return "WARN"
        return "OK"


def build_screens(state: SystemState):
    disk_temps = {d.name: d.temp_c for d in state.disks if d.temp_c is not None}
    disk_max = max(disk_temps.values()) if disk_temps else 0
    disk_count = len(state.disks)
    status = HealthEngine.calculate(state)
    screens = []

    # 0: STATUS
    screens.append((
        render_line(f"NAS {status} {state.cpu.temp_c or 0}C"),
        render_line(f"POOL {state.storage.used_pct:.0f}% {state.storage.used_bytes/(1024**4):.1f}T")
    ))

    # 1: STORAGE
    total_tb = state.storage.total_bytes / (1024**4)
    used_tb = state.storage.used_bytes / (1024**4)
    screens.append((
        render_line(f"POOL {used_tb:.1f}/{total_tb:.1f}T"),
        render_line(f"USED {state.storage.used_pct:.0f}% FREE {state.storage.free_bytes/(1024**4):.1f}T")
    ))

    # 2: DISKS
    screens.append((
        render_line(f"DISKS {disk_count} OK"),
        render_line(f"MAX {disk_max}C")
    ))

    # 3: SYSTEM (CPU + RAM)
    screens.append((
        render_line(f"CPU {state.cpu.usage_pct:.0f}% {state.cpu.temp_c or 0}C"),
        render_line(f"RAM {state.memory.used_pct:.0f}% {state.memory.available_mb/1024:.1f}G")
    ))

    # 4: NETWORK
    rx_mb = state.network.rx_bps / (1024 * 1024)
    tx_mb = state.network.tx_bps / (1024 * 1024)
    screens.append((
        render_line(f"NET {rx_mb:.1f}M {tx_mb:.1f}M"),
        render_line(f"LAN {state.network.ip}")
    ))

    # 5: TORRENT
    dl_mb = state.torrent.dl_speed / (1024 * 1024)
    if state.torrent.torrent_name:
        screens.append((
            render_line(f"TOR {state.torrent.active_torrents} DL{dl_mb:.1f}M"),
            render_line(f"{state.torrent.torrent_name[:16]}")
        ))
    else:
        screens.append((
            render_line(f"TOR IDLE"),
            render_line(f"UP {state.torrent.ul_speed/(1024*1024):.1f}M")
        ))

    # 6: FAN
    screens.append((
        render_line(f"FAN {state.fan.pwm or 0}% {state.fan.rpm}"),
        render_line(f"CPU {state.cpu.temp_c or 0}C")
    ))

    return screens
