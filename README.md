# DX4000 LCD Dashboard

Dashboard modular para el LCD 16x2 del WD Sentinel DX4000.

## Estructura Modular

```
dx4000-lcd/
├── main.py              # Punto de entrada del daemon
├── nas_lcd.py          # Script legacy (deprecated)
├── formatters.py        # Formateo de valores (temperatura, velocidad, bytes)
├── bar.py              # Generación de barras CGRAM
├── dx4000_lcd/
│   ├── __init__.py
│   ├── state.py        # Modelos de datos (SystemState, CpuState, etc.)
│   ├── renderer.py     # Renderizado de líneas (fit_line, lcd_escape)
│   ├── health.py       # Motor de evaluación de salud (HealthEngine)
│   ├── lcdproc.py     # Transport LCDproc
│   ├── screen_manager.py # Navegación entre pantallas
│   ├── collectors/     # Recolectores de datos del sistema
│   │   ├── __init__.py
│   │   ├── torrents.py
│   │   └── ...
│   └── screens/       # Pantallas del dashboard
│       ├── status.py
│       ├── storage.py
│       ├── system.py
│       ├── network.py
│       ├── torrent.py
│       ├── disks.py
│       └── alert.py
└── tests/             # Pruebas y scripts de diagnóstico
```

## Uso

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar daemon
python3 main.py
```

## Configuración

- **LCD_HOST**: `127.0.0.1`
- **LCD_PORT**: `13666`
- **INTERVAL**: Segundos entre cambios de pantalla (default: 3)

## Screens Disponibles

1. **status** - Estado general (CPU, disco más caliente, almacenamiento)
2. **storage** - Uso de almacenamiento con barra
3. **disk** - Información SMART del disco más caliente
4. **system** - CPU, load, memoria
5. **network** - Velocidad RX/TX
6. **torrent** - Estado de qBittorrent

## Problemas conocidos y soluciones

### 1. Protocolo LCDproc (Escapado de espacios)
El protocolo de LCDproc es estricto. Al enviar widgets mediante `widget_set`, los espacios en el texto deben ser escapados con una barra invertida (`\ `) para que el daemon no los interprete como separadores de argumentos.
* **Error:** `widget_set dash hd 1 1 CPU 31C P14` (causa fallo o renderizado incorrecto)
* **Solución:** `widget_set dash hd 1 1 CPU\ 31C\ P14`

### 2. Configuración LCDd (Size y Contrast)
El driver `hd44780` para el wiring Winamp del DX4000 requiere configuraciones específicas:
* **Size**: Debe ser `16x2`. Usar `20x4` hará que la segunda línea no sea visible o se desplace erróneamente.
* **Contrast**: Es necesario ajustar `Contrast=800` (o similar, dependiendo de la unidad) en `/etc/LCDd.conf` para asegurar visibilidad en la línea 2.

### 3. Hardware/Wiring
Si tras aplicar el escapado de espacios y el `Size=16x2` correcto no se ve la segunda línea, verificar:
1. Conexión física del cable paralelo (Winamp wiring).
2. Potenciómetro de contraste físico del LCD.
