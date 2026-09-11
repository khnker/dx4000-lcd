#!/usr/bin/env python3
import socket
import time
import subprocess
import re
import os
from pathlib import Path

from dx4000_lcd.renderer import fit_line, lcd_escape
from dx4000_lcd.formatters import format_temp, format_speed, format_bytes, format_percent
from dx4000_lcd.bar import render_bar
from dx4000_lcd.screens import ScreenOutput
from dx4000_lcd.screens.status import StatusScreen
from dx4000_lcd.screens.storage import StorageScreen
from dx4000_lcd.screens.system import SystemScreen
from dx4000_lcd.screens.network import NetworkScreen
from dx4000_lcd.screens.torrent import TorrentScreen
from dx4000_lcd.screens.disks import DiskScreen
from dx4000_lcd.state import SystemState, CpuState, DiskState, StorageState, TorrentState, NetworkState, FanState
from dx4000_lcd.collectors import CpuCollector, DiskTempCollector, FanCollector, StorageCollector

HOST = "127.0.0.1"
PORT = 13666
SCREEN_INTERVAL = 5
SCREENS = ["status", "storage", "system", "network"]


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5).stdout.strip()


class TorrentCollector:
    def read(self, state):
        try:
            out = subprocess.run(
                ["curl", "-s", "http://127.0.0.1:8080/api/v2/transfer/info"],
                capture_output=True, text=True, timeout=3
            ).stdout
            import json
            data = json.loads(out)
            state.torrent.dl_speed = data.get("dl_info_speed", 0) * 1024
            state.torrent.ul_speed = data.get("ul_info_speed", 0) * 1024
        except Exception:
            pass


class NetworkCollector:
    def __init__(self):
        self.prev_rx = None
        self.prev_tx = None
        self.prev_time = None

    def read(self, state):
        try:
            with open("/proc/net/dev") as f:
                for line in f:
                    if "eth0" in line or "enp" in line:
                        parts = line.split()
                        rx = int(parts[1])
                        tx = int(parts[9])
                        now = time.monotonic()
                        if self.prev_rx is not None:
                            dt = now - self.prev_time
                            if dt > 0:
                                state.network.rx_bps = int((rx - self.prev_rx) / dt)
                                state.network.tx_bps = int((tx - self.prev_tx) / dt)
                        self.prev_rx = rx
                        self.prev_tx = tx
                        self.prev_time = now
                        break
        except Exception:
            pass
        state.network.ip = sh("hostname -I").split()[0] if sh("hostname -I") else "???"


CGRAM_GLYPHS = [
    ("BAR1",    "16 16 16 16 16 16 16 16"),
    ("BAR2",    "24 24 24 24 24 24 24 24"),
    ("BAR3",    "28 28 28 28 28 28 28 28"),
    ("BAR4",    "30 30 30 30 30 30 30 30"),
    ("THERMO",  "4 4 4 4 14 14 31 14"),
    ("FAN",     "10 4 10 0 0 0 0 0"),
    ("NET",     "17 10 4 21 4 10 17 0"),
    ("WARN",    "4 14 21 4 4 0 4 0"),
]


def lcd_connect():
    s = socket.create_connection((HOST, PORT), timeout=5)
    lcd_send(s, "hello")
    lcd_send(s, "client_set -name nas-dash")
    lcd_send(s, "screen_add dash")
    lcd_send(s, "screen_set dash -priority alert")
    lcd_send(s, "widget_add dash L1 string")
    lcd_send(s, "widget_add dash L2 string")
    time.sleep(0.5)
    for slot, (name, rows) in enumerate(CGRAM_GLYPHS):
        lcd_send(s, f"set_char {slot} {rows}")
        time.sleep(0.1)
    return s


def lcd_send(s, cmd):
    s.sendall((cmd + "\n").encode())


def main():
    state = SystemState()
    collectors = [CpuCollector(), DiskTempCollector(), FanCollector(), StorageCollector(), TorrentCollector(), NetworkCollector()]

    screen_index = 0
    last_lines = None
    s = lcd_connect()

    while True:
        try:
            for c in collectors:
                try:
                    c.read(state)
                except Exception:
                    pass

            if screen_index >= len(SCREENS):
                screen_index = 0

            screen_name = SCREENS[screen_index]
            if screen_name == "status":
                out = StatusScreen().render(state)
            elif screen_name == "storage":
                out = StorageScreen().render(state)
            elif screen_name == "system":
                out = SystemScreen().render(state)
            elif screen_name == "network":
                out = NetworkScreen().render(state)
            else:
                out = StatusScreen().render(state)

            lines = (out.line1, out.line2)
            if lines != last_lines:
                lcd_send(s, f"widget_set dash L1 1 1 {out.line1}")
                lcd_send(s, f"widget_set dash L2 1 2 {out.line2}")
                last_lines = lines

            screen_index += 1
            time.sleep(SCREEN_INTERVAL)

        except Exception:
            time.sleep(5)
            try:
                s = lcd_connect()
                last_lines = None
            except Exception:
                time.sleep(5)


if __name__ == "__main__":
    main()
