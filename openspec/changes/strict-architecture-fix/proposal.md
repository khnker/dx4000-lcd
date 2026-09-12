# Proposal: Strict Architecture Fix & UX Alignment

## Goal
Enforce strict separation of concerns, eliminating all remaining architectural leaks (CGRAM hardcoding in main, manual dispatch in ScreenManager, silent failures in collectors) and preparing the foundation for Phase 3 (LCD UX v1).

## Scope
1. **CGRAM Encapsulation**: Move raw slot definitions and patterns to `dx4000_lcd/cgram.py`. Provide `load_cgram(lcd)`. `main.py` only calls `load_cgram(lcd)`.
2. **Dynamic Screen Dispatch**: Refactor `ScreenManager` to use a registered dictionary of screen instances instead of `if/elif` statements.
3. **Collector Robustness**: Replace silent `except Exception: pass` with proper logging and state marking (`stale` flag or timestamp) in collectors.
4. **Legacy Purge**: Ensure `run_lcd.py` and `nas_lcd.py` are completely removed from workspace and deployment paths.
