CGRAM_GLYPHS = {
    0: "16 16 16 16 16 16 16 16",     # BAR_25
    1: "24 24 24 24 24 24 24 24",     # BAR_50
    2: "28 28 28 28 28 28 28 28",     # BAR_75
    3: "30 30 30 30 30 30 30 30",     # BAR_100
    4: "4 4 4 4 14 14 31 14",        # TEMP
    5: "10 4 10 0 0 0 0 0",          # FAN
    6: "0 4 14 31 14 4 0 0",         # DOWNLOAD
    7: "0 4 4 4 14 31 14 0",         # UPLOAD
}

def load_cgram(lcd):
    for slot, rows in CGRAM_GLYPHS.items():
        lcd.set_char(slot, rows)
