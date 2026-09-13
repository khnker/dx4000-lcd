from typing import Dict

# Iconos mapeados a slots CGRAM (0-7)
CGRAM_PATTERNS: Dict[str, str] = {
    "BAR1": "16 16 16 16 16 16 16 16",
    "BAR2": "24 24 24 24 24 24 24 24",
    "BAR3": "28 28 28 28 28 28 28 28",
    "BAR4": "30 30 30 30 30 30 30 30",
    "THERMO": "4 4 4 4 14 14 31 14",
    "FAN": "10 4 10 0 0 0 0 0",
    "ARROW_DOWN": "04040404150E0400",
    "ARROW_UP": "040E150404040400",
}

def load_cgram(lcd):
    slots = {
        0: "BAR1",
        1: "BAR2",
        2: "BAR3",
        3: "BAR4",
        4: "THERMO",
        5: "FAN",
        6: "ARROW_DOWN",
        7: "ARROW_UP",
    }
    for slot, name in slots.items():
        if name in CGRAM_PATTERNS:
            lcd.set_char(slot, CGRAM_PATTERNS[name])
