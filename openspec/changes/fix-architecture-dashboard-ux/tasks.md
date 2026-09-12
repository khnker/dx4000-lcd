# Tasks: fix-architecture-dashboard-ux

## Task 1: ScreenManager Orchestration
- [ ] Remove all screen imports from `main.py` (keep only LCDProc, ScreenManager, HealthEngine, collectors)
- [ ] Remove all `if/elif` screen dispatch from `main.py`
- [ ] ScreenManager.render(state, health_results) decides what to show internally
- [ ] ScreenManager internally imports and dispatches screens

## Task 2: HealthEngine Coverage
- [ ] HealthEngine evaluates CPU temperature (existing)
- [ ] HealthEngine evaluates disk temperatures
- [ ] HealthEngine evaluates fan RPM (0 = error)
- [ ] HealthEngine evaluates storage percentage (>90% = warn, >95% = error)
- [ ] HealthResult includes source and message

## Task 3: Data Availability States
- [ ] Replace all `except: pass` with error logging
- [ ] Add `available` flag to state objects (True/False)
- [ ] Display "--" or "N/A" instead of 0 for unavailable data
- [ ] HealthEngine treats unavailable data as UNKNOWN, not OK

## Task 4: CGRAM Centralization
- [ ] All CGRAM patterns in `dx4000_lcd/cgram.py`
- [ ] LCDProc.load_cgram() loads all 8 slots
- [ ] Remove CGRAM patterns from `main.py`

## Task 5: StatusScreen Redesign
- [ ] Remove "NAS" prefix (waste of space)
- [ ] Show: `CPU 42C D45C` (CPU temp, hottest disk)
- [ ] Show: `STO 72% F1.2K` (storage %, fan RPM)

## Task 6: StorageScreen Redesign
- [ ] Use CGRAM bar: `██████████░░`
- [ ] Format: `STORAGE 72%` + bar on line 2

## Task 7: TorrentScreen Redesign
- [ ] Distinguish OFFLINE/IDLE/DOWNLOADING states
- [ ] Show: `TOR OFFLINE` when qBittorrent unreachable
- [ ] Show: `TOR IDLE` when no active torrents
- [ ] Show: `DL 12.4M 73%` + scrolling name
- [ ] Implement scroll for long names (>12 chars)

## Task 8: SystemScreen Redesign
- [ ] Show: `CPU 37% 42C` (usage %, temp)
- [ ] Show: `RAM 61% L0.42` (memory %, load)
- [ ] Handle unavailable data gracefully

## Task 9: NetworkScreen Redesign
- [ ] Clearly show RX on line 1, TX on line 2
- [ ] Format: `RX 12.4M` / `TX 1.2M`

## Task 10: AlertScreen Improvements
- [ ] Show actual data causing alert: `!! DISK HOT !!` + `sda 52C`
- [ ] NOT: `CHECK disk`
- [ ] Add alert expiration (max 5 seconds, then return to rotation)

## Task 11: Rotation Timing
- [ ] STATUS: 4s
- [ ] STORAGE: 3s
- [ ] TORRENT: 5s (more time for scroll)
- [ ] SYSTEM: 3s
- [ ] NETWORK: 3s

## Task 12: qBittorrent States
- [ ] Check if qBittorrent API reachable
- [ ] State: OFFLINE (API down)
- [ ] State: IDLE (no active torrents)
- [ ] State: DOWNLOADING (active torrents)
- [ ] Show appropriate message for each

## Task 13: Configuration
- [ ] Move qBittorrent credentials to config (not hardcoded)
- [ ] Keep LCD_HOST, LCD_PORT configurable

## Task 14: Legacy Cleanup
- [ ] Ensure no `run_lcd.py` in repo
- [ ] Ensure no `nas_lcd.py` in repo
- [ ] Ensure no `__pycache__` tracked

## Acceptance Criteria
- [ ] main.py does NOT import StatusScreen, StorageScreen, etc.
- [ ] main.py does NOT have if/elif for screens
- [ ] ScreenManager.render() is the ONLY rendering decision point
- [ ] HealthEngine covers cpu, disk, fan, storage
- [ ] Unavailable data shows as "--" or "N/A", not 0
- [ ] All screens redesigned for 16x2
- [ ] AlertScreen expires after max 5 seconds
- [ ] qBittorrent shows OFFLINE/IDLE/DOWNLOADING states
- [ ] CGRAM patterns in cgram.py only
- [ ] No silent except:pass
