import time
import socket
import logging
from dx4000_lcd.state import SystemState
from dx4000_lcd.collectors import (
    CpuCollector, MemoryCollector, DiskTempCollector, FanCollector,
    StorageCollector, NetworkCollector, UptimeCollector
)
from dx4000_lcd.collectors.torrents import TorrentCollector
from dx4000_lcd.renderer import build_screens

LCD_HOST = "127.0.0.1"
LCD_PORT = 13666
SCREEN_INTERVAL = 4

logging.basicConfig(
    filename="/tmp/nas_lcd.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def send(s, cmd):
    s.sendall((cmd + "\n").encode())
    logging.debug("SENT: %s", cmd)

def main():
    logging.info("Starting modular nas_lcd daemon v2")
    state = SystemState()
    fast_collectors = [
        CpuCollector(),
        MemoryCollector(),
        FanCollector(),
        StorageCollector(mountpoint="/mnt/media"),
        NetworkCollector(),
        TorrentCollector(),
        UptimeCollector(),
    ]
    slow_collectors = [
        DiskTempCollector(),
    ]
    screen_idx = 0

    while True:
        try:
            s = socket.create_connection((LCD_HOST, LCD_PORT), timeout=5)
            send(s, "hello")
            send(s, "client_set -name nas-dash")
            send(s, "screen_add dash")
            send(s, "screen_set dash -priority alert")
            send(s, "widget_add dash hd string")
            send(s, "widget_add dash hd2 string")
            time.sleep(0.5)

            slow_tick = 0
            while True:
                for c in fast_collectors:
                    try:
                        c.read(state)
                    except Exception as e:
                        logging.error("Collector %s: %s", c.__class__.__name__, e)

                slow_tick += 1
                if slow_tick % 10 == 0:
                    for c in slow_collectors:
                        try:
                            c.read(state)
                        except Exception as e:
                            logging.error("Collector %s: %s", c.__class__.__name__, e)

                screens = build_screens(state)
                l1, l2 = screens[screen_idx]
                send(s, "widget_set dash hd 1 1 " + l1)
                send(s, "widget_set dash hd2 1 2 " + l2)
                screen_idx = (screen_idx + 1) % len(screens)
                time.sleep(SCREEN_INTERVAL)

        except Exception as e:
            logging.error("LCD error: %s", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
