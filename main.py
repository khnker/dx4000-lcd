import time
import logging
from dx4000_lcd.lcdproc import LCDProc
from dx4000_lcd.screen_manager import ScreenManager
from dx4000_lcd.health import HealthEngine, highest_priority_alert
from dx4000_lcd.state import SystemState
from dx4000_lcd.collectors import CpuCollector, DiskCollector, FanCollector, StorageCollector, MemoryCollector, NetworkCollector, TorrentCollector, UptimeCollector
from dx4000_lcd.cgram import load_cgram

logging.basicConfig(level=logging.INFO)

def main():
    state = SystemState()
    collectors = [
        CpuCollector(),
        MemoryCollector(),
        FanCollector(),
        DiskCollector(),
        StorageCollector(),
        NetworkCollector(),
        TorrentCollector(),
        UptimeCollector(),
    ]

    lcd = LCDProc()
    manager = ScreenManager()
    engine = HealthEngine()

    while True:
        try:
            lcd.connect()
            load_cgram(lcd)

            while True:
                for c in collectors:
                    try:
                        c.read(state)
                    except Exception as e:
                        logging.warning(f"Collector {c.__class__.__name__} failed: {e}")

                health_results = engine.evaluate(state)
                top_alert = highest_priority_alert(health_results)

                output = manager.render(state, health_results)
                lcd.update(output.line1, output.line2)

                time.sleep(3)
                manager.next()

        except Exception as e:
            logging.error(f"LCD error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
