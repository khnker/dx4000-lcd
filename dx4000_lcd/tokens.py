from typing import Optional, Any


class TemperatureToken:
    WIDTH = 4
    SUFFIX = "C"

    @staticmethod
    def render(value: Optional[float]) -> str:
        if value is None:
            return f"{'--':>4}"
        try:
            v = int(round(value))
        except (ValueError, TypeError):
            return f"{'--':>4}"
        return f"{v:>3}{TemperatureToken.SUFFIX}"


class PercentToken:
    WIDTH = 4
    SUFFIX = "%"

    @staticmethod
    def render(value: Optional[float]) -> str:
        if value is None:
            return f"{'--':>{PercentToken.WIDTH}}"
        try:
            v = int(round(value))
        except (ValueError, TypeError):
            return f"{'--':>{PercentToken.WIDTH}}"
        return f"{v:>{PercentToken.WIDTH-1}}{PercentToken.SUFFIX}"


class SpeedToken:
    WIDTH = 8

    @staticmethod
    def render(bytes_per_sec: Optional[int]) -> str:
        if not bytes_per_sec:
            return f"{'0B/s':>{SpeedToken.WIDTH}}"
        value = float(bytes_per_sec)
        for unit in ("B/s", "K/s", "M/s", "G/s"):
            if value < 1000:
                if value < 10:
                    return f"{value:>6.1f}{unit}"
                elif value < 100:
                    return f"{value:>5.0f}{unit}"
                else:
                    return f"{value:>4.0f}{unit}"
            value /= 1000
        return f"{value:>4.1f}T/s"


class BytesToken:
    WIDTH = 6

    @staticmethod
    def render(bytes_val: Optional[int]) -> str:
        if bytes_val is None:
            return f"{'--':>{BytesToken.WIDTH}}"
        value = float(bytes_val)
        for unit in ("B", "K", "M", "G", "T"):
            if value < 1024:
                if value < 10:
                    return f"{value:>5.1f}{unit}"
                else:
                    return f"{value:>4.0f}{unit}"
            value /= 1024
        return f"{value:>5.1f}P"


class DiskToken:
    WIDTH = 4

    @staticmethod
    def render(name: str) -> str:
        if not name:
            return f"{'--':>{DiskToken.WIDTH}}"
        n = name.replace("/dev/", "")
        if len(n) > DiskToken.WIDTH:
            n = n[:DiskToken.WIDTH]
        return f"{n:>{DiskToken.WIDTH}}"


class StateToken:
    WIDTH = 6

    STATES = {
        "ok": "OK",
        "warn": "WARN",
        "error": "FAIL",
        "unknown": "----",
        "idle": "IDLE",
        "active": "ACTV",
        "offline": "OFF ",
    }

    @staticmethod
    def render(state: Optional[str]) -> str:
        if not state:
            return f"{'--':>{StateToken.WIDTH}}"
        s = str(state).lower()
        return StateToken.STATES.get(s, s[:StateToken.WIDTH].upper().ljust(StateToken.WIDTH))


class CountToken:
    WIDTH = 3

    @staticmethod
    def render(count: Optional[int]) -> str:
        if count is None:
            return f"{'--':>{CountToken.WIDTH}}"
        return f"{count:>{CountToken.WIDTH}}"


class LabelToken:
    WIDTH = 4

    @staticmethod
    def render(label: str) -> str:
        return f"{label[:LabelToken.WIDTH]:<{LabelToken.WIDTH}}"


class LoadToken:
    WIDTH = 5

    @staticmethod
    def render(load: Optional[float]) -> str:
        if load is None:
            return f"{'--':>{LoadToken.WIDTH}}"
        try:
            l = float(load)
        except (ValueError, TypeError):
            return f"{'--':>{LoadToken.WIDTH}}"
        if l < 10:
            return f"L{l:>4.2f}"
        return f"L{l:>4.1f}"


class FanToken:
    WIDTH = 5

    @staticmethod
    def render(rpm: Optional[int]) -> str:
        if rpm is None or rpm == 0:
            return f"{'--':>{FanToken.WIDTH}}"
        if rpm >= 1000:
            return f"{rpm // 1000}K"
        return f"{rpm}"


class ValueToken:
    WIDTH = 6

    @staticmethod
    def render(value: Optional[float]) -> str:
        if value is None:
            return f"{'--':>{ValueToken.WIDTH}}"
        try:
            return f"{value:>{ValueToken.WIDTH - 1}.1f}"
        except (ValueError, TypeError):
            return f"{'--':>{ValueToken.WIDTH}}"


class DirectionToken:
    WIDTH = 4

    DIRECTIONS = {
        "down": "DOWN",
        "up": "UP",
        "dl": "DOWN",
        "ul": "UP",
    }

    @staticmethod
    def render(direction: Optional[str]) -> str:
        if not direction:
            return f"{'--':>{DirectionToken.WIDTH}}"
        d = str(direction).lower()
        result = DirectionToken.DIRECTIONS.get(d, d[:DirectionToken.WIDTH].upper())
        return result.ljust(DirectionToken.WIDTH)


class CapacityToken:
    WIDTH = 6

    @staticmethod
    def render(bytes_val: Optional[int]) -> str:
        if bytes_val is None:
            return f"{'--':>{CapacityToken.WIDTH}}"
        value = float(bytes_val)
        for unit in ("T", "G", "M", "K", "B"):
            if value >= 1024 or unit == "B":
                if unit == "B" and value < 1024:
                    if value < 10:
                        return f"{value:>5.1f}B"
                    return f"{value:>4.0f}B"
                value /= 1024 if unit != "B" else 1
            if value < 1024:
                if value < 10:
                    return f"{value:>5.1f}{unit}"
                elif value < 100:
                    return f"{value:>4.0f}{unit}"
                return f"{value:>3.1f}{unit}"
        return f"{value:>5.1f}T"
