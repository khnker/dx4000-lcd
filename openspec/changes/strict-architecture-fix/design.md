# Design: Strict Architecture Fix

## Architecture Pipeline
`Collectors` → `SystemState` → `HealthEngine` → `ScreenManager` → `Screen` → `LCDProc` → `LCD`

## Components
1. **`dx4000_lcd/cgram.py`**:
   - Holds `CGRAM_GLYPHS` dictionary mapping slot IDs to row values.
   - Exposes `load_cgram(lcd: LCDProc)`.
2. **`dx4000_lcd/screen_manager.py`**:
   - Uses a registry dict: `self._screens = {"status": StatusScreen(), ...}`.
   - Renders active screen via `.render(state)`.
3. **`dx4000_lcd/collectors/`**:
   - Base or individual collectors log exceptions via `logging.error()` and update a `last_success` or `stale` flag on their respective state nodes.
