import time
import socket
import logging
from dx4000_lcd.state import SystemState
from dx4000_lcd.collectors import CpuCollector, DiskTempCollector, FanCollector, StorageCollector
from dx4000_lcd.collectors.torrents import TorrentCollector
from dx4000_lcd.renderer import build_screens, ScrollText

LCD_HOST = "127.0.0.1"
LCD_PORT = 13666
INTERVAL = 3

logging.basicConfig(
    filename="/tmp/nas_lcd.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def send(s, cmd):
    s.sendall((cmd + "\n").encode())
    logging.debug("SENT: %s", cmd)

def main():
    logging.info("Starting modular nas_lcd daemon")
    state = SystemState()
    scroll = ScrollText(speed=2)
    collectors = [
        CpuCollector(),
        DiskTempCollector(),
        FanCollector(),
        StorageCollector(mountpoint="/mnt/media"),
        TorrentCollector(),
    ]

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

            while True:
                for c in collectors:
                    try:
                        c.read(state)
                    except Exception as e:
                        logging.error("Collector %s: %s", c.__class__.__name__, e)

                # Actualizar scroll siempre (incluso si no se muestra TORRENT)
                scroll.update(state.torrent.torrent_name)

                screens = build_screens(state, scroll)
                for l1, l2 in screens:
                    send(s, "widget_set dash hd 1 1 " + l1)
                    send(s, "widget_set dash hd2 1 2 " + l2)
                    time.sleep(INTERVAL)

        except Exception as e:
            logging.error("LCD error: %s", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
