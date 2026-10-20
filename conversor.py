"""Módulo de lógica para la conversión de medidas de longitud (mm, cm, m).
Diseñado para proyectos de robótica y aplicaciones generales.
"""

import sys

FACTORES_A_METROS = {
    'mm': 0.001,
    'cm': 0.01,
    'm': 1.0
}

UNIDADES_VALIDAS = tuple(FACTORES_A_METROS.keys())


def convertir(valor: float | int | str, unidad_origen: str, unidad_destino: str) -> float:
    """Convierte un valor de longitud entre mm, cm y m.

    :param valor: Valor numérico a convertir (acepta int, float o str con punto o coma decimal).
    :param unidad_origen: Unidad actual ('mm', 'cm', 'm').
    :param unidad_destino: Unidad a la que se desea convertir ('mm', 'cm', 'm').
    :return: Valor numérico convertido.
    :raises ValueError: Si alguna unidad no es válida o si el valor no es numérico.
    """
    origen = str(unidad_origen).strip().lower()
    destino = str(unidad_destino).strip().lower()

    if origen not in FACTORES_A_METROS:
        raise ValueError(f"Unidad de origen no válida: '{unidad_origen}'. Permitidas: {', '.join(UNIDADES_VALIDAS)}")

    if destino not in FACTORES_A_METROS:
        raise ValueError(f"Unidad de destino no válida: '{unidad_destino}'. Permitidas: {', '.join(UNIDADES_VALIDAS)}")

    # Normalizar si viene como string (soporte para coma decimal como '2,5')
    if isinstance(valor, str):
        valor = valor.strip().replace(',', '.')

    try:
        val_float = float(valor)
    except (TypeError, ValueError) as err:
        raise ValueError(f"El valor '{valor}' no es un número válido. Introduzca solo números.") from err

    # Conversión a metros como unidad base y luego a unidad destino
    valor_en_metros = val_float * FACTORES_A_METROS[origen]
    resultado = valor_en_metros / FACTORES_A_METROS[destino]

    # Redondeo para evitar artefactos de punto flotante de IEEE 754
    return round(resultado, 6)


def main():
    """Interfaz de línea de comandos (CLI) con captura de errores amigable."""
    if len(sys.argv) < 4:
        print("Uso: py conversor.py <valor> <unidad_origen> <unidad_destino>")
        print("Ejemplo: py conversor.py 500 mm cm")
        print(f"Unidades disponibles: {', '.join(UNIDADES_VALIDAS)}")
        sys.exit(0)

    val_arg = sys.argv[1]
    origen_arg = sys.argv[2]
    destino_arg = sys.argv[3]

    try:
        resultado = convertir(val_arg, origen_arg, destino_arg)
        print(f"{resultado} {destino_arg}")
    except ValueError as e:
        print(f"Error de conversión: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
