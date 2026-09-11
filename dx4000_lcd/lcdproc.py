import socket
from .renderer import lcd_escape, fit_line

class LCDProc:
    def __init__(self, host="127.0.0.1", port=13666):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=5)
        self.send("hello")
        self.send("client_set -name nas-dash")
        self.send("screen_add dash")
        self.send("screen_set dash -priority alert")
        self.send("widget_add dash L1 string")
        self.send("widget_add dash L2 string")

    def send(self, cmd):
        if self.sock:
            self.sock.sendall((cmd + "\n").encode())

    def set_line(self, row: int, text: str):
        escaped = lcd_escape(fit_line(text))
        self.send(f"widget_set dash L{row} 1 {row} {{{escaped}}}")

    def set_char(self, slot: int, rows: list[int]):
        row_str = " ".join(map(str, rows))
        self.send(f"set_char {slot} {row_str}")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None