CGRAM_GLYPHS = {
    0: "16 16 16 16 16 16 16 16",  # BAR1
    1: "24 24 24 24 24 24 24 24",  # BAR2
    2: "28 28 28 28 28 28 28 28",  # BAR3
    3: "30 30 30 30 30 30 30 30",  # BAR4
    4: "4 4 4 4 14 14 31 14",      # THERMO
    5: "10 4 10 0 0 0 0 0",        # FAN
    6: "0 0 0 0 0 0 0 0",          # SPARE
    7: "0 0 0 0 0 0 0 0",          # SPARE
}

def load_cgram(lcd):
    for slot, rows in CGRAM_GLYPHS.items():
        lcd.set_char(slot, rows)
