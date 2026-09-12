# Proposal: Fix Architecture & Dashboard UX

## Problem
The LCD dashboard has multiple architectural and UX issues:

### Architectural Problems
1. `main.py` directly imports and dispatches all screens (violates encapsulation)
2. `ScreenManager` uses manual `if/elif` instead of real orchestration
3. CGRAM patterns still in `main.py` instead of `cgram.py`
4. HealthEngine only evaluates CPU, ignores disks/fan/storage
5. Multiple `except: pass` silently hide failures

### UX Problems (16x2 LCD)
1. LCD treated as terminal, not dashboard
2. Status screen wastes space (shows "NAS" prefix)
3. Storage screen doesn't use CGRAM bars
4. Torrent screen doesn't scroll, shows limited info
5. Network screen doesn't distinguish RX/TX clearly
6. System screen missing RAM and CPU %
7. Temperature shows "0°C" instead of "--" when unavailable
8. AlertScreen can dominate forever without expiration

### Robustness Problems
1. hwmon paths hardcoded (hwmon0/hwmon1)
2. DiskTempCollector fragile
3. qBittorrent credentials hardcoded
4. Can't distinguish OFFLINE/IDLE/DOWNLOADING states

## Solution

### Phase 1: Architectural Fixes
1. Make `ScreenManager.render(state, health)` the ONLY rendering decision point
2. Remove all screen dispatch from `main.py`
3. Move CGRAM to `dx4000_lcd/cgram.py`
4. Implement proper error handling (no silent failures)
5. Complete HealthEngine to cover disks/fan/storage
6. Add data availability states (STALE/UNKNOWN vs 0)

### Phase 2: UX Improvements
1. Redesign 6 screens for 16x2 real estate:
   - **STATUS**: `CPU 42C D45C` + `STO 72% F1.2K`
   - **STORAGE**: `STORAGE 72%` + `██████████░░` (CGRAM bar)
   - **TORRENT**: Show DL speed, progress, scroll name
   - **SYSTEM**: `CPU 37% 42C` + `RAM 61% L0.42`
   - **NETWORK**: `RX 12.4M` + `TX 1.2M`
   - **ALERT**: `!! DISK HOT !!` + `sda 52C`
2. Implement scroll for long torrent names
3. Add rotation timing (Torrent gets more time)
4. Add alert expiration mechanism

### Phase 3: Robustness
1. Dynamic hwmon device discovery
2. qBittorrent ONLINE/OFFLINE/IDLE/DOWNLOADING states
3. Externalize credentials to config

## Scope
### Included
- ScreenManager real orchestration
- HealthEngine coverage (cpu, disk, fan, storage)
- CGRAM centralization
- Error handling with stale states
- UX redesign of all 6 screens
- Alert expiration
- Proper data availability (not showing 0 as real)

### Excluded
- BackupCollector
- MemoryCollector (beyond what's needed for SystemScreen)
- NetworkCollector (beyond what's needed)
- DiskSMARTCollector
- New sensors
- systemd changes
- Web UI / API

## Expected Outcome
```
main.py → manager.render(state, health) → Screen → LCDProc → LCD 16x2
```

All screens show real data or explicit unavailable states. No silent failures.
