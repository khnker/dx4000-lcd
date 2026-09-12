# Tasks: Strict Architecture Fix

- [ ] Create `dx4000_lcd/cgram.py` and move patterns there.
- [ ] Implement `load_cgram(lcd)` and refactor `main.py` to use it.
- [ ] Refactor `ScreenManager` to use a screen registry dict instead of `if/elif`.
- [ ] Update collectors to remove `except: pass` and add error logging/stale tracking.
- [ ] Final purge of legacy files: `run_lcd.py`, `nas_lcd.py`.
- [ ] Verify `__pycache__` and `*.pyc` removal.
- [ ] Run full test suite for architecture compliance.
