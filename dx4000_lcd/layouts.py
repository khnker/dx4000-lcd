from dx4000_lcd.tokens import (
    LabelToken, TemperatureToken, PercentToken, DiskToken,
    StateToken, CountToken, SpeedToken, BytesToken, LoadToken,
    FanToken, DirectionToken,
)


# STANDARD family

def layout_standard_2x2(label1: str, val1: str, label2: str, val2: str) -> tuple[str, str]:
    l1 = label1[:4].ljust(4)
    l2 = label2[:4].ljust(4)
    line1 = f"{l1} {val1[:6]}"
    line2 = f"{l2} {val2[:6]}"
    return line1, line2


def layout_status(cpu_temp: str, fan_rpm: str, disk_temp: str, storage_pct: str) -> tuple[str, str]:
    return (
        f"CPU {cpu_temp} FAN {fan_rpm}",
        f"DSK {disk_temp} STO {storage_pct}",
    )


def layout_disk(disk: str, temp: str, state: str) -> tuple[str, str]:
    return (
        f"DISK {disk} {temp}",
        f"SMART {state}",
    )


def layout_system(cpu_pct: str, cpu_temp: str, ram_pct: str, load: str) -> tuple[str, str]:
    return (
        f"CPU {cpu_pct} {cpu_temp}",
        f"RAM {ram_pct} {load}",
    )


def layout_network(rx: str, tx: str) -> tuple[str, str]:
    return (rx, tx)


def layout_alert(source: str, state: str) -> tuple[str, str]:
    return (f"! {source}", state[:15])


# TORRENT family

def layout_torrent(state_str: str, speed: str) -> tuple[str, str]:
    return (state_str, speed)


# MERGERFS family

def layout_storage(pct: str, free: str) -> tuple[str, str]:
    return (f"POOL {pct} USED", f"FREE {free}")


def layout_storage_mergerfs(pct: str, free: str, total: str) -> tuple[str, str]:
    return (f"POOL {pct} USED", f"FREE {free} / {total}")
