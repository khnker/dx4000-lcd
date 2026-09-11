#!/usr/bin/env python3
import socket
import time

HOST = "127.0.0.1"
PORT = 13666

ICONS = {
    "FAN": [
        [10, 4, 10, 0, 0, 0, 0, 0],
        [10, 4, 14, 21, 14, 4, 10, 0],
        [4, 21, 14, 4, 14, 21, 4, 0],
        [4, 14, 21, 4, 21, 14, 4, 0],
    ],
    "WARN": [
        [4, 14, 21, 4, 4, 0, 4, 0],
        [4, 14, 14, 17, 31, 4, 4, 0],
        [4, 14, 14, 17, 17, 31, 0, 0],
        [4, 14, 21, 21, 21, 14, 4, 0],
    ],
    "THERMO": [
        [4, 4, 4, 4, 4, 14, 14, 31],
        [4, 4, 4, 4, 4, 14, 14, 31],
        [14, 14, 4, 4, 4, 4, 14, 31],
    ],
    "NET": [
        [17, 10, 4, 21, 4, 10, 17, 0],
        [17, 10, 4, 31, 4, 10, 17, 0],
        [17, 17, 10, 4, 10, 17, 17, 0],
    ],
}


def send(sock, command):
    sock.sendall(command.encode())


def set_char(sock, slot, glyph):
    values = " ".join(map(str, glyph))
    send(sock, f"set_char {slot} {values}\n")


def clear(sock):
    send(sock, "widget_set S L1 1 1 {                }\n")
    send(sock, "widget_set S L2 1 1 {                }\n")


def show(sock, line1, line2):
    clear(sock)
    send(sock, f"widget_set S L1 1 1 {{{line1:<16}}}\n")
    send(sock, f"widget_set S L2 1 1 {{{line2:<16}}}\n")


def main():
    print("Conectando a LCDd.")

    sock = socket.create_connection((HOST, PORT), timeout=5)

    send(sock, "hello\n")
    time.sleep(0.2)
    send(sock, "client_set -name cgram-tester\n")
    send(sock, "screen_add S\n")
    send(sock, "screen_set S -priority 128\n")
    send(sock, "widget_add S L1 string\n")
    send(sock, "widget_add S L2 string\n")
    time.sleep(0.5)

    slot = 4

    for icon_name, variants in ICONS.items():
        print()
        print("=" * 50)
        print(f"  {icon_name}")
        print("=" * 50)

        for index, glyph in enumerate(variants, start=1):
            print(f"  Variante {index}: {glyph}")
            set_char(sock, slot, glyph)
            time.sleep(0.2)
            show(sock, f"{icon_name} V{index}", "TEST: " + chr(slot) + " OK?")
            print("  Mira el LCD.")
            print("  ENTER = siguiente | q + ENTER = salir")
            answer = input("> ").strip().lower()
            if answer == "q":
                break
        if answer == "q":
            break

    clear(sock)
    send(sock, "screen_del S\n")
    send(sock, "client_del\n")
    sock.close()
    print("\nTester terminado.")


if __name__ == "__main__":
    main()
