from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.renderer import fit_line
from dx4000_lcd.tokens import PercentToken, BytesToken
from dx4000_lcd.layouts import layout_storage, layout_storage_mergerfs


class StorageScreen:
    def render(self, state) -> ScreenOutput:
        storage = getattr(state, "storage", None)
        if not storage:
            return ScreenOutput(
                line1=fit_line("POOL --% USED"),
                line2=fit_line("FREE --"),
            )
        used_pct = storage.used_pct
        free_bytes = storage.free_bytes or 0
        total_bytes = storage.total_bytes or 0
        pct_str = PercentToken.render(used_pct)
        free_str = BytesToken.render(free_bytes)

        if getattr(storage, "mergerfs", False):
            total_str = BytesToken.render(total_bytes)
            line1, line2 = layout_storage_mergerfs(pct_str, free_str, total_str)
        else:
            line1, line2 = layout_storage(pct_str, free_str)

        return ScreenOutput(
            line1=fit_line(line1),
            line2=fit_line(line2),
        )
