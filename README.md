# DX4000 LCD Dashboard

Dashboard para el LCD 16x2 del WD Sentinel DX4000.

## Problemas conocidos y soluciones

### 1. Protocolo LCDproc (Escapado de espacios)
El protocolo de LCDproc es estricto. Al enviar widgets mediante `widget_set`, los espacios en el texto deben ser escapados con una barra invertida (`\ `) para que el daemon no los interprete como separadores de argumentos.
* **Error:** `widget_set dash hd 1 1 CPU 31C P14` (causa fallo o renderizado incorrecto)
* **Solución:** `widget_set dash hd 1 1 CPU\ 31C\ P14`

### 2. Configuración LCDd (Size y Contrast)
El driver `hd44780` para el wiring Winamp del DX4000 requiere configuraciones específicas:
* **Size**: Debe ser `16x2`. Usar `20x4` hará que la segunda línea no sea visible o se desplace erróneamente.
* **Contrast**: Es necesario ajustar `Contrast=800` (o similar, dependiendo de la unidad) en `/etc/LCDd.conf` para asegurar visibilidad en la línea 2.

### 3. Estructura de archivos y Módulos
* **Conflictos de Importación**: Se debe evitar crear directorios con el mismo nombre que los módulos `.py` (ej: no tener `dx4000_lcd/` directorio y `dx4000_lcd.py` archivo al mismo tiempo).
* **Servicio systemd**: Asegurarse de que el script instalado en `/usr/local/bin/` sea ejecutable (`chmod +x`).

### 4. Hardware/Wiring
Si tras aplicar el escapado de espacios y el `Size=16x2` correcto no se ve la segunda línea, verificar:
1. Conexión física del cable paralelo (Winamp wiring).
2. Potenciómetro de contraste físico del LCD.
