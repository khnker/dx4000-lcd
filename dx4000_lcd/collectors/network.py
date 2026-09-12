# NetworkCollector - reads network stats with auto-detection of primary interface
import logging
import socket
import os
import time
from dx4000_lcd.state import SystemState

class NetworkCollector:
    def __init__(self, interface=None):
        self.interface = interface or self._detect_primary_interface()
        self._prev_rx = None
        self._prev_tx = None
        self._prev_time = None

    def _detect_primary_interface(self) -> str:
        """Detect primary network interface (default route)."""
        try:
            # Read default route interface from /proc
            with open("/proc/net/route", "r") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 2 and parts[1] == "00000000":  # default route
                        iface = parts[0]
                        if iface and iface != "lo":
                            return iface
        except Exception:
            pass
        
        # Fallback: try common interface names
        for iface in ["eth0", "enp0s3", "ens33", "eno1"]:
            if os.path.exists(f"/sys/class/net/{iface}"):
                return iface
        
        return "eth0"  # ultimate fallback

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
