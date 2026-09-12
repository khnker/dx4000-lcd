# NetworkCollector - reads network stats from /proc/net/dev
import logging
from dx4000_lcd.state import SystemState
import socket

class NetworkCollector:
    def __init__(self, interface="eth0"):
        self.interface = interface
        self._prev_rx = None
        self._prev_tx = None
        self._prev_time = None

    def read(self, state: SystemState):
        try:
            # Get IP address
            try:
                state.network.ip = socket.gethostbyname(socket.gethostname())
            except:
                state.network.ip = "N/A"

            # Get traffic stats
            with open("/proc/net/dev") as f:
                for line in f:
                    if self.interface in line:
                        parts = line.split()
                        rx = int(parts[1])
                        tx = int(parts[9])
                        
                        # Calculate speed if we have previous values
                        import time
                        now = time.monotonic()
                        if self._prev_rx is not None and self._prev_time:
                            dt = now - self._prev_time
                            if dt > 0:
                                state.network.rx_bps = (rx - self._prev_rx) / dt
                                state.network.tx_bps = (tx - self._prev_tx) / dt
                        
                        self._prev_rx = rx
                        self._prev_tx = tx
                        self._prev_time = now
                        break
        except Exception as e:
            logging.warning(f"NetworkCollector failed: {e}")
