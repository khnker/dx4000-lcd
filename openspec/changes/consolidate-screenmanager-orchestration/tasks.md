# Tasks: consolidate-screenmanager-orchestration

## Task 1: Refactor ScreenManager.render()
- [ ] Move screen dispatch logic from main.py to ScreenManager.render()
- [ ] ScreenManager.render() accepts (state, alerts) parameters
- [ ] ScreenManager decides AlertScreen vs normal screen based on alerts

## Task 2: Centralize CGRAM
- [ ] Create dx4000_lcd/cgram.py with CGRAM patterns
- [ ] LCDProc.load_cgram() method
- [ ] Remove hardcoded CGRAM from main.py

## Task 3: Error Handling
- [ ] Replace except Exception: pass with proper error logging
- [ ] Mark collector state as STALE on error

## Task 4: Cleanup Legacy Files
- [ ] Delete run_lcd.py from repo
- [ ] Delete nas_lcd.py from repo
- [ ] Remove __pycache__ from tracking
- [ ] Update .gitignore

## Task 5: Verify Pipeline
- [ ] Test that main.py works with new architecture
- [ ] Verify alerts interrupt normal screen rotation
