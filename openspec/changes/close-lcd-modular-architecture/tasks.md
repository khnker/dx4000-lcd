# Tasks: close-lcd-modular-architecture

## Task 1: ScreenManager.render()
- [ ] ScreenManager.render(state, health) recibe SystemState y HealthReport
- [ ] Eliminar if/elif dispatch de screens desde main.py
- [ ] ScreenManager decide AlertScreen vs normal screen

## Task 2: AlertScreen
- [ ] Crear/integrar AlertScreen
- [ ] Recibir HealthReport y presentar alerta
- [ ] Formatos: "! DISK HOT", "! FAN ERROR", "! STORAGE 92%"

## Task 3: Prioridad de alertas
- [ ] HealthEngine produce estados: OK/WARN/ERROR/UNKNOWN
- [ ] ScreenManager prioriza: ERROR > WARN > UNKNOWN > OK
- [ ] Alerta interrumpe rotación temporalmente

## Task 4: CGRAM centralizado
- [ ] Crear dx4000_lcd/cgram.py con patrones
- [ ] LCDProc.load_cgram() method
- [ ] Eliminar patrones de main.py

## Task 5: LCDProc API
- [ ] lcd.update(line1, line2) es única interfaz
- [ ] Encapsular connect/disconnect/send/widget

## Task 6: Limpiar renderer.py
- [ ] Solo utilidades: fit_line, lcd_escape, format_*
- [ ] Eliminar lógica de health/collector/screen

## Task 7: Main como composition root
- [ ] Solo inicialización y loop
- [ ] Llama manager.render(state, health)
- [ ] No conoce screens, protocolo, thresholds

## Task 8: Error handling
- [ ] Reemplazar except Exception: pass
- [ ] Log warnings en collectors
- [ ] State marcado como stale en error

## Task 9: Legacy cleanup
- [ ] Eliminar run_lcd.py
- [ ] Eliminar nas_lcd.py
- [ ] Eliminar __pycache__ tracked
- [ ] .gitignore excluye __pycache__/

## Task 10: Tests
- [ ] test_health.py - OK/WARN/ERROR/UNKNOWN
- [ ] test_screen_manager.py - alert priority
- [ ] test_alert_screen.py - formatting
- [ ] test_renderer.py - fit_line/lcd_escape
- [ ] test_cgram.py - 8 slots
- [ ] test_lcdproc.py - sin hardware

## Criterios de aceptación
- [ ] main.py no selecciona screens
- [ ] main.py no contiene patrones CGRAM
- [ ] ScreenManager.render() es punto único
- [ ] Única implementación de HealthEngine
- [ ] screens no conocen LCDproc
- [ ] collectors no conocen LCDproc
- [ ] Alertas priorizan sobre screens normales
- [ ] No existe except Exception: pass
- [ ] run_lcd.py/nas_lcd.py eliminados
- [ ] __pycache__ no versionado
- [ ] Todos los tests pasan
