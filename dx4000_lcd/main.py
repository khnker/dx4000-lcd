from dx4000_lcd.collectors import collect
from dx4000_lcd.renderer import build_screens
from dx4000_lcd.state import NasState

LCD_HOST = "127.0.0.1"
LCD_PORT = 13666
INTERVAL = 3


def send(s, cmd):
    s.sendall((cmd + "\n").encode())


def main():
    import socket
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    while True:
        try:
            state = collect()
            screens = build_screens(state)
            l1, l2 = screens[0]

            s = socket.create_connection((LCD_HOST, LCD_PORT), timeout=5)
            send(s, "hello")
            send(s, "client_set -name nas-dash")
            send(s, "screen_add dash")
            send(s, "screen_set dash -priority alert")
            send(s, "widget_add dash hd string")
            send(s, "widget_add dash hd2 string")

            # Espacios escapados con \ (requerido por protocolo LCDproc)
            l1_esc = l1.replace(" ", "\\ ")
            l2_esc = l2.replace(" ", "\\ ")

            send(s, f"widget_set dash hd 1 1 {l1_esc}")
            send(s, f"widget_set dash hd2 1 2 {l2_esc}")
            s.close()
            time.sleep(INTERVAL)
        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()