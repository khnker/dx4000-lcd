# Proposal: Complete Collector Integration

## Problem
The dashboard has architectural leaks:
1. Duplicate collector implementations (in __init__.py and separate files)
2. Not all collectors are instantiated in main.py
3. Legacy nas_lcd.py still exists
4. Hardcoded hardware paths still present in some collectors

## Solution
1. Remove duplicate collector code from __init__.py
2. Ensure all collectors are imported and instantiated in main.py
3. Delete legacy nas_lcd.py
4. Connect all screens properly through ScreenManager

## Scope
- Delete collectors/__init__.py monolithic implementation
- Create individual collector files for memory, network, torrents, uptime
- Connect all collectors in main.py
- Remove legacy nas_lcd.py
- Ensure ScreenManager handles all screen routing
