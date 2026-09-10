# DX4000 LCD Dashboard

Sistema de monitoreo para el NAS WD DX4000 con pantalla LCD 16x2 (HD44780, wiring Winamp).

## Hardware

- LCD: HD44780 compatible, 16x2
- Paralelo: 0x378 (parport0)
- Driver: hd44780 via LCDd (LCDproc)

## Archivos

- `nas_lcd.py` - Script principal (funcional)
- `LCDd.conf` - Configuración del daemon LCDd
- `nas-lcd.service` - Service file systemd

## Despliegue en .101

```bash
# Copiar script
scp nas_lcd.py root@10.10.10.101:/usr/local/bin/nas_lcd.py

# Copiar config LCDd
scp LCDd.conf root@10.10.10.101:/etc/LCDd.conf

# Copiar service
scp nas-lcd.service root@10.10.10.101:/etc/systemd/system/nas-lcd.service

# En el NAS
systemctl daemon-reload
systemctl restart lcdproc.service
systemctl restart nas-lcd.service
```

## Requisitos

- `smartctl` (smartmontools) para temperaturas de disco
- `lcdproc` + `lcdproc-extra-drivers` para el daemon LCD

## Pantalla

```
L1: CPU 31C P14    (temperatura CPU + PWM fan)
L2: DSK 41C 14%    (temp max disco + uso storage)
```

## Bug conocido

Los espacios en el texto deben escaparse con `\` para el protocolo LCDproc:
```python
# Correcto
l1 = f"CPU {temp}C".replace(" ", "\\ ")

# Incorrecto (LCDd ignora el comando)
l1 = f"CPU {temp}C"
```
