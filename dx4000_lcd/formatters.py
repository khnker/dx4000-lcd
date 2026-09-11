from typing import Optional


def format_temp(value: Optional[float]) -> str:
    if value is None:
        return "--C"
    return f"{round(value):02d}C"


def format_speed(bytes_per_second: Optional[int]) -> str:
    if not bytes_per_second:
        return "0B/s"
    value = float(bytes_per_second)
    for unit in ("B/s", "K/s", "M/s", "G/s"):
        if value < 1000:
            return f"{value:.1f}{unit}" if value < 100 else f"{value:.0f}{unit}"
        value /= 1000
    return f"{value:.1f}T/s"


def format_bytes(value: Optional[int]) -> str:
    if value is None:
        return "--"
    value = float(value)
    for unit in ("B", "K", "M", "G", "T"):
        if value < 1024:
            return f"{value:.1f}{unit}"
        value /= 1024
    return f"{value:.1f}P"


def format_percent(value: Optional[float]) -> str:
    if value is None:
        return "--%"
    return f"{round(value):d}%"
