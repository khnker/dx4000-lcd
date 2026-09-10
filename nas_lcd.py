#!/usr/bin/env python3
import os
import subprocess
import time
import logging
import socket

LCD_HOST = "127.0.0.1"
LCD_PORT = 13666
INTERVAL = 3

logging.basicConfig(
    filename="/tmp/nas_lcd.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

def get_core_temp():
    try:
        return int(open("/sys/class/hwmon/hwmon0/temp2_input").read().strip()) // 1000
    except:
        return 0

def get_fan_pwm():
    try:
        return int(open("/sys/class/hwmon/hwmon1/pwm2").read().strip())
    except:
        return 0

def get_disk_max_temp():
    devs = "/dev/sda /dev/sdb /dev/sdd /dev/sde /dev/sdf".split()
    mx = 0
    for dev in devs:
        try:
            out = subprocess.run(["smartctl", "-A", dev], capture_output=True, text=True, timeout=2).stdout
            for ln in out.splitlines():
                if "Temperature_Celsius" in ln:
                    p = ln.split()
                    t = int(p[len(p)-1])
                    if t > mx:
                        mx = t
        except:
            pass
    return mx

def get_storage_pct():
    try:
        total = 0
        used = 0
        for ln in sh("df -P -x tmpfs -x devtmpfs").splitlines()[1:]:
            c = ln.split()
            if len(c) >= 4 and c[0].startswith("/dev/sd"):
                used += int(c[2]) * 1024
                total += int(c[1]) * 1024
        return int(used * 100 / total) if total else 0
    except:
        return 0

def send(s, cmd):
    s.sendall((cmd + "\n").encode())
    logging.debug("SENT: %s", cmd)

def main():
    logging.info("Starting nas_lcd main loop")
    while True:
        try:
            s = socket.create_connection((LCD_HOST, LCD_PORT), timeout=5)
            send(s, "hello")
            send(s, "client_set -name nas-dash")
            send(s, "screen_add dash")
            send(s, "screen_set dash -priority alert")
            send(s, "widget_add dash hd string")
            send(s, "widget_add dash hd2 string")
            time.sleep(0.5)
            while True:
                temp = get_core_temp()
                pwm = get_fan_pwm()
                disk_max = get_disk_max_temp()
                ov = get_storage_pct()

                # Espacios escapados con \ (requerido por protocolo LCDproc)
                l1 = f"CPU {temp:02d}C P{pwm:02d}".replace(" ", "\\ ")
                l2 = f"DSK {disk_max:02d}C {ov:02d}%".replace(" ", "\\ ")

                send(s, f"widget_set dash hd 1 1 {l1}")
                send(s, f"widget_set dash hd2 1 2 {l2}")
                time.sleep(INTERVAL)
        except Exception as e:
            logging.error("Main loop exception: %s", e)
            time.sleep(3)

if __name__ == "__main__":
    main()
