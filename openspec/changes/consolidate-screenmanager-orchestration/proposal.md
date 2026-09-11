# Proposal: Consolidate ScreenManager Orchestration

## Problem
The current `main.py` contains too much orchestration logic:
- Screen dispatch (if/else for each screen type)
- Health alert evaluation but not integrated into rendering
- CGRAM definitions hardcoded in main loop

## Solution
1. Move screen dispatch logic to `ScreenManager.render(state, alerts)`
2. Integrate HealthEngine alerts to interrupt normal rotation
3. Centralize CGRAM patterns in `dx4000_lcd/cgram.py`
4. Replace `except Exception: pass` with proper error handling

## Scope
- Refactor ScreenManager to handle all rendering decisions
- Centralize CGRAM in dedicated module
- Clean up legacy files (run_lcd.py, nas_lcd.py)
- Add proper error handling in collectors

## Out of Scope
- Backup functionality
- New collectors (Memory, Network, DiskSMART)
- Advanced configuration

## Expected Outcome
```
┌──────────────┐
 │ Collectors │
 └──────┬───────┘
 ↓
 ┌──────────────┐
 │ SystemState │
 └──────┬───────┘
 ↓
 ┌──────────────┐
 │ HealthEngine │
 └──────┬───────┘
 ↓
 ┌──────────────┐
 │ScreenManager │
 └──────┬───────┘
 ↓
 Screen
 ↓
 LCDProc
```

Main.py should only:
- Initialize components
- Run the loop
- Call manager.render(state, alerts)
- Send result to LCDProc
