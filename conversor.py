"""Módulo de lógica para la conversión de medidas de longitud (mm, cm, m).
Diseñado para proyectos de robótica y aplicaciones generales.
"""

FACTORES_A_METROS = {
    'mm': 0.001,
    'cm': 0.01,
    'm': 1.0
}

UNIDADES_VALIDAS = tuple(FACTORES_A_METROS.keys())


def convertir(valor: float, unidad_origen: str, unidad_destino: str) -> float:
    """Convierte un valor de longitud entre mm, cm y m.

    :param valor: Valor numérico a convertir.
    :param unidad_origen: Unidad actual ('mm', 'cm', 'm').
    :param unidad_destino: Unidad a la que se desea convertir ('mm', 'cm', 'm').
    :return: Valor numérico convertido.
    :raises ValueError: Si alguna unidad no es válida o si el valor no es numérico.
    """
    origen = str(unidad_origen).strip().lower()
    destino = str(unidad_destino).strip().lower()

    if origen not in FACTORES_A_METROS:
        raise ValueError(f"Unidad de origen no válida: '{unidad_origen}'. Permitidas: {UNIDADES_VALIDAS}")

    if destino not in FACTORES_A_METROS:
        raise ValueError(f"Unidad de destino no válida: '{unidad_destino}'. Permitidas: {UNIDADES_VALIDAS}")

    try:
        val_float = float(valor)
    except (TypeError, ValueError) as err:
        raise ValueError(f"El valor a convertir debe ser un número válido: {valor}") from err

    # Conversión a metros como unidad base y luego a unidad destino
    valor_en_metros = val_float * FACTORES_A_METROS[origen]
    resultado = valor_en_metros / FACTORES_A_METROS[destino]

    # Redondeo para evitar artefactos de punto flotante de IEEE 754
    return round(resultado, 6)

