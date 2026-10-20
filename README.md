# Conversor de Medidas de Longitud (mm, cm, m)
**Robots Móviles Autónomos — CIFT Misericordia**

Este proyecto implementa y reproduce la especificación BDD (Gherkin) para la conversión de medidas de longitud:

```gherkin
Característica: Conversión de medidas de longitud (mm, cm, m)

  Escenario: Convertir milímetros a centímetros
    Dado que el usuario introduce el valor 500
    Y la unidad de origen es "mm"
    Y la unidad de destino es "cm"
    Cuando se solicita la conversión
    Entonces el resultado obtenido debe ser 50.0

  Escenario: Convertir metros a milímetros
    Dado que el usuario introduce el valor 2.5
    Y la unidad de origen es "m"
    Y la unidad de destino es "mm"
    Cuando se solicita la conversión
    Entonces el resultado obtenido debe ser 2500.0

  Escenario: Limpiar la zona de resultado
    Dado que existe un resultado de conversión "100 cm"
    Cuando el usuario presiona el botón de limpiar
    Entonces la zona de resultado debe quedar vacía
```

---

## Archivos del Proyecto

- **[conversor.py](conversor.py)**: Lógica principal de conversión matemática y validación de unidades.
- **[app_gui.py](app_gui.py)**: Aplicación gráfica de escritorio (Tkinter) con los campos, selectores, botones y zona de resultado.
- **[test_conversor.py](test_conversor.py)**: Batería de pruebas automatizadas que ejecutan y validan cada escenario BDD paso a paso.
- **[index.html](index.html)**: Aplicación web interactiva que se puede abrir directamente en cualquier navegador.

---

## Cómo ejecutar

### 1. Ejecutar las pruebas automatizadas (BDD)
Para comprobar que los 3 escenarios pasan con éxito:
```powershell
py test_conversor.py
```

### 2. Ejecutar la aplicación de escritorio (GUI Tkinter)
```powershell
py app_gui.py
```

### 3. Ejecutar desde consola (CLI)
```powershell
py conversor.py 500 mm cm
py conversor.py 2,5 m mm
```

### 4. Abrir la versión Web
Haz doble clic en `index.html` o ábrelo en cualquier navegador (Chrome, Edge, Firefox).

---

## Control de Errores y Validaciones
- **Entradas no numéricas**: Se gestionan amigablemente informando al usuario en vez de interrumpir la aplicación.
- **Coma decimal**: Soporte nativo para formatos con coma (ej. `2,5`) o punto (ej. `2.5`).
- **Unidades admitidas**: `mm`, `cm`, `m`.


