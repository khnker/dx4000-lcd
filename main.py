import time
from dx4000_lcd.lcdproc import LCDProc
from dx4000_lcd.screen_manager import ScreenManager
from dx4000_lcd.health import HealthEngine, highest_priority_alert
from dx4000_lcd.screens.status import StatusScreen
from dx4000_lcd.screens.storage import StorageScreen
from dx4000_lcd.screens.system import SystemScreen
from dx4000_lcd.screens.network import NetworkScreen
from dx4000_lcd.screens.torrent import TorrentScreen
from dx4000_lcd.screens.alert import AlertScreen
from dx4000_lcd.state import SystemState
from dx4000_lcd.collectors import CpuCollector, DiskTempCollector, FanCollector, StorageCollector

def main():
    state = SystemState()
    collectors = [
        CpuCollector(),
        DiskTempCollector(),
        FanCollector(),
        StorageCollector(),
    ]
    
    lcd = LCDProc()
    manager = ScreenManager()
    engine = HealthEngine()
    
    status_screen = StatusScreen()
    storage_screen = StorageScreen()
    system_screen = SystemScreen()
    network_screen = NetworkScreen()
    torrent_screen = TorrentScreen()
    alert_screen = AlertScreen()

    while True:
        try:
            lcd.connect()
            
            # Cargar CGRAM (Glyphs)
            lcd.set_char(0, "16 16 16 16 16 16 16 16")
            lcd.set_char(1, "24 24 24 24 24 24 24 24")
            lcd.set_char(2, "28 28 28 28 28 28 28 28")
            lcd.set_char(3, "30 30 30 30 30 30 30 30")
            lcd.set_char(4, "4 4 4 4 14 14 31 14")
            lcd.set_char(5, "10 4 10 0 0 0 0 0")
            
            while True:
                # Recolectar datos
                for c in collectors:
                    try:
                        c.read(state)
                    except Exception:
                        pass
                
                # Evaluar salud / alertas
                alerts = engine.evaluate(state)
                top_alert = highest_priority_alert(alerts)
                
                if top_alert:
                    out = alert_screen.render(top_alert)
                else:
                    name = manager.current_screen_name
                    if name == "status":
                        out = status_screen.render(state)
                    elif name == "storage":
                        out = storage_screen.render(state)
                    elif name == "system":
                        out = system_screen.render(state)
                    elif name == "network":
                        out = network_screen.render(state)
                    else:
                        out = status_screen.render(state)
                        
                lcd.update(out.line1, out.line2)
                time.sleep(3)
                manager.next()
                
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    main()
