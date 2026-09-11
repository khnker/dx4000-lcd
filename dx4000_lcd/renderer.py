LCD_WIDTH = 16

def fit_line(text: str, width: int = LCD_WIDTH) -> str:
    return text[:width].ljust(width)

def lcd_escape(text: str) -> str:
    return text.replace(" ", "\\ ")

def render_line(text: str) -> str:
    return lcd_escape(fit_line(text))
