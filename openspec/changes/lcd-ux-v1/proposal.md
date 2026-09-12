# Proposal: LCD UX v1 - Visual Improvements for 16x2 Dashboard

## Goal
Redesign all 6 screens to maximize information density on 16x2 LCD, use CGRAM bars effectively, improve readability, and add scrolling for long content.

## Screens Redesign

### 1. StatusScreen
**Current:** `NAS 42C 45C` / `STO 72%`
**New:**
```
CPU 42C D45C
STO 72% F1.2K
```
- Remove "NAS" prefix (waste of space)
- Show CPU temp + hottest disk temp
- Show storage % + fan RPM

### 2. StorageScreen
**Current:** `STO 72%` / `4.2T/5.8T`
**New:**
```
STORAGE 72%
██████████░░░
```
- Use CGRAM bar (10 chars + padding)

### 3. TorrentScreen
**New States:**
- `TOR OFFLINE` / `qBIT DOWN` (API unreachable)
- `TOR IDLE` / `0 ACTIVE` (no torrents)
- `DL 12.4M 73%` / `ubuntu-24.04` (scrolling name)
- Scroll long names (>12 chars)

### 4. SystemScreen
**Current:** `CPU 42C` / `LOAD 0.42`
**New:**
```
CPU 37% 42C
RAM 61% L0.42
```
- Show CPU usage %
- Show RAM percentage
- Show load

### 5. NetworkScreen
**Current:** `NET 12.3M` / `NET 1.2M`
**New:**
```
RX 12.4M
TX  1.2M
```
- Clear RX/TX labels
- Proper spacing

### 6. AlertScreen
**Current:** `! CPU HOT` / `CHECK cpu`
**New:**
```
!! DISK HOT!!
sda 52C > 45C
```
- Show actual data causing alert
- Show threshold if applicable
- Max 5 seconds then return to rotation

## Rotation Timing
- STATUS: 4s
- STORAGE: 3s
- TORRENT: 5s (more time for scroll)
- SYSTEM: 3s
- NETWORK: 3s

## Data Availability
- Show `--` or `N/A` instead of `0` for unavailable data
- 0°C is dangerous (looks like real data)
