CGRAM_GLYPHS = {
    0: "16 16 16 16 16 16 16 16",     # BAR_20 (1 column filled)
    1: "24 24 24 24 24 24 24 24",     # BAR_40 (2 columns)
    2: "28 28 28 28 28 28 28 28",     # BAR_60 (3 columns)
    3: "30 30 30 30 30 30 30 30",     # BAR_80 (4 columns = full)
    4: "4 4 4 4 14 14 31 14",        # TEMP
    5: "10 4 10 0 0 0 0 0",          # FAN
    6: "0 4 14 31 14 4 0 0",         # DOWNLOAD (arrow down)
    7: "0 4 4 4 14 31 14 0",         # UPLOAD (arrow up)
}

def load_cgram(lcd):
    for slot, rows in CGRAM_GLYPHS.items():
        lcd.set_char(slot, rows)
