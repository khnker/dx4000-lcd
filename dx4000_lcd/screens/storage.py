from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.formatters import format_bytes
from dx4000_lcd.bar import render_bar


def _val(obj):
    if obj is None:
        return None
    if hasattr(obj, "value"):
        return obj.value
    return obj


class StorageScreen:
    def render(self, state) -> ScreenOutput:
        storage = getattr(state, "storage", None)
        used_pct = _val(getattr(storage, "used_pct", None) if storage is not None else None)
        if used_pct is None:
            pct = None
            pct_text = "--%"
        else:
            pct = round(used_pct)
            pct_text = f"{pct}%"

        used_bytes = _val(getattr(storage, "used_bytes", None) if storage is not None else None)
        if used_bytes is not None:
            line1 = f"STO {pct_text} {format_bytes(used_bytes)}"
            if len(line1) > 16:
                line1 = f"STO {pct_text}"
        else:
            line1 = f"STO {pct_text}"

        bar_pct = pct if pct is not None else 0
        return ScreenOutput(
            line1=fit_line(line1),
            line2=fit_line(render_bar(bar_pct, 10)),
        )
