# StorageCollector - reads storage stats with proper mergerfs detection
import subprocess
import logging
import os
from dx4000_lcd.state import SystemState, StorageState

STORAGE_PATH = "/mnt/media"

class StorageCollector:
    def read(self, state: SystemState):
        try:
            if not os.path.ismount(STORAGE_PATH):
                logging.warning(f"StorageCollector: {STORAGE_PATH} not mounted")
                state.storage = StorageState(
                    mountpoint=STORAGE_PATH,
                    total_bytes=0,
                    used_bytes=0,
                    free_bytes=0,
                    mergerfs=False
                )
                return

            # Detect filesystem type using findmnt
            fs_type = "unknown"
            try:
                result = subprocess.run(
                    ["findmnt", "-T", STORAGE_PATH, "-no", "FSTYPE"],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                fs_type = result.stdout.strip().lower()
            except Exception as e:
                logging.warning(f"StorageCollector: findmnt failed: {e}")

            is_mergerfs = fs_type == "mergerfs"

            # Get storage stats
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
                        mergerfs=is_mergerfs
                    )
                else:
                    raise ValueError("Unexpected df output format")
            else:
                raise ValueError("No df output")
        except Exception as e:
            logging.warning(f"StorageCollector failed: {e}")
            state.storage = StorageState(
                mountpoint=STORAGE_PATH,
                total_bytes=0,
                used_bytes=0,
                free_bytes=0,
                mergerfs=False
            )
