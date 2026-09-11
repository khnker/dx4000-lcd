import socket
from dx4000_lcd.renderer import lcd_escape

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

    def set_char(self, slot: int, rows: str):
        self.send(f"set_char {slot} {rows}")

    def update(self, line1: str, line2: str):
        # Escape spaces for LCDProc protocol
        self.send(f"widget_set dash L1 1 1 {lcd_escape(line1)}")
        self.send(f"widget_set dash L2 1 2 {lcd_escape(line2)}")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
