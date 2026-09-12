import subprocess
import logging
import os
from dx4000_lcd.state import SystemState, StorageState

STORAGE_PATH = "/mnt/media"

class StorageCollector:
    def __init__(self):
        self._last_success = 0

    def read(self, state: SystemState):
        try:
            if not os.path.ismount(STORAGE_PATH):
                logging.warning(f"StorageCollector: {STORAGE_PATH} not mounted")
                state.storage = StorageState(mountpoint=STORAGE_PATH, total_bytes=0, used_bytes=0, free_bytes=0)
                return

            result = subprocess.run(
                ["df", "-B1", STORAGE_PATH],
                capture_output=True,
                text=True,
                timeout=5
            )
            lines = result.stdout.strip().splitlines()
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 4:
                    state.storage = StorageState(
                        mountpoint=STORAGE_PATH,
                        total_bytes=int(parts[1]),
                        used_bytes=int(parts[2]),
                        free_bytes=int(parts[3]),
                        mergerfs=True
                    )
            self._last_success = self._last_success
        except Exception as e:
            logging.warning(f"StorageCollector failed: {e}")
            state.storage = StorageState(mountpoint=STORAGE_PATH, total_bytes=0, used_bytes=0, free_bytes=0)
