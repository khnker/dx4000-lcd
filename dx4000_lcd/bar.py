LCD_WIDTH = 16

def render_bar(percent: float, width: int = 9) -> str:
    percent = max(0.0, min(100.0, percent))
    pixels = round(percent / 100.0 * width * 5)
    result = []
    for _ in range(width):
        filled = min(5, pixels)
        if filled == 0:
            result.append(" ")
        elif filled >= 4:
            result.append(chr(3))
        else:
            result.append(chr(filled - 1))
        pixels -= filled
    return "".join(result)
