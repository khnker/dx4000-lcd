# Proposal: Cerrar arquitectura modular del LCD

## Problem
El dashboard LCD actual tiene múltiples problemas arquitectónicos:
- `main.py` contiene lógica de dispatch de screens
- CGRAM hardcoded en el loop principal
- HealthEngine no está integrado con ScreenManager
- Múltiples entrypoints legacy (run_lcd.py, nas_lcd.py)
- Excepciones silenciadas en collectors

## Solution
1. Convertir ScreenManager en única autoridad de rendering
2. Integrar HealthEngine con ScreenManager
3. Centralizar CGRAM en módulo dedicado
4. Eliminar dispatch desde main.py
5. Limpiar legacy files

## Scope
### Incluido
- ScreenManager.render(state, health) como punto único
- AlertScreen integrada por prioridad
- CGRAM encapsulado en cgram.py
- LCDProc como único transporte
- Eliminar run_lcd.py, nas_lcd.py
- Corregir manejo de excepciones
- Limpiar __pycache__
- Tests de arquitectura

### Excluido (fuera de scope)
- BackupCollector/BackupScreen
- MemoryCollector
- NetworkCollector  
- DiskSMARTCollector nuevo
- Nuevos sensores/pantallas
- systemd
- Web UI / API / Prometheus / MQTT

## Expected Outcome
```
Collectors → SystemState → HealthEngine → ScreenManager → Screen → LCDProc → LCD 16×2
```

main.py debe ser solo composition root + loop, sin lógica de negocio.
