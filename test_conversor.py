"""Pruebas automatizadas (BDD / Unit Tests) para el conversor de medidas de longitud.
Reproduce con exactitud los escenarios especificados en el requerimiento Gherkin:
- Conversión de milímetros a centímetros (500 mm -> 50.0 cm)
- Conversión de metros a milímetros (2.5 m -> 2500.0 mm)
- Limpieza de la zona de resultado
"""

import unittest
import tkinter as tk
from conversor import convertir
from app_gui import ConversorApp


class TestConversorBDD(unittest.TestCase):
    """Pruebas unitarias directas sobre la lógica de conversión."""

    def test_escenario_convertir_milimetros_a_centimetros(self):
        """Escenario: Convertir milímetros a centímetros
        Dado que el usuario introduce el valor 500
        Y la unidad de origen es "mm"
        Y la unidad de destino es "cm"
        Cuando se solicita la conversión
        Entonces el resultado obtenido debe ser 50.0
        """
        # Dado
        valor = 500
        unidad_origen = "mm"
        unidad_destino = "cm"

        # Cuando
        resultado = convertir(valor, unidad_origen, unidad_destino)

        # Entonces
        self.assertEqual(resultado, 50.0)

    def test_escenario_convertir_metros_a_milimetros(self):
        """Escenario: Convertir metros a milímetros
        Dado que el usuario introduce el valor 2.5
        Y la unidad de origen es "m"
        Y la unidad de destino es "mm"
        Cuando se solicita la conversión
        Entonces el resultado obtenido debe ser 2500.0
        """
        # Dado
        valor = 2.5
        unidad_origen = "m"
        unidad_destino = "mm"

        # Cuando
        resultado = convertir(valor, unidad_origen, unidad_destino)

        # Entonces
        self.assertEqual(resultado, 2500.0)

    def test_otras_conversiones_validas(self):
        """Pruebas adicionales de cobertura entre todas las combinaciones mm, cm y m."""
        # 100 cm a m -> 1.0
        self.assertEqual(convertir(100, "cm", "m"), 1.0)
        # 1 m a cm -> 100.0
        self.assertEqual(convertir(1, "m", "cm"), 100.0)
        # 10 mm a mm -> 10.0
        self.assertEqual(convertir(10, "mm", "mm"), 10.0)
        # 1500 mm a m -> 1.5
        self.assertEqual(convertir(1500, "mm", "m"), 1.5)

    def test_errores_en_unidades_o_valores_invalidos(self):
        """Validación de manejo de errores."""
        with self.assertRaises(ValueError):
            convertir(10, "km", "m")
        with self.assertRaises(ValueError):
            convertir(10, "m", "yardas")
        with self.assertRaises(ValueError):
            convertir("invalido", "mm", "cm")


class TestConversorGUI(unittest.TestCase):
    """Pruebas de integración sobre la interfaz gráfica que reproducen la interacción del usuario."""

    @classmethod
    def setUpClass(cls):
        # Crear root oculto para ejecutar pruebas de widgets sin ventana visible
        cls.root = tk.Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except Exception:
            pass

    def setUp(self):
        self.app = ConversorApp(self.root)

    def test_gui_escenario_convertir_milimetros_a_centimetros(self):
        """Reproducción en GUI del Escenario 1:
        Introduce 500, origen mm, destino cm -> resultado 50.0 cm / 50.0 numérico.
        """
        self.app.valor_var.set("500")
        self.app.origen_var.set("mm")
        self.app.destino_var.set("cm")

        self.app.solicitar_conversion()

        self.assertEqual(self.app.ultimo_resultado_num, 50.0)
        self.assertIn("50.0", self.app.resultado_var.get())

    def test_gui_escenario_convertir_metros_a_milimetros(self):
        """Reproducción en GUI del Escenario 2:
        Introduce 2.5, origen m, destino mm -> resultado 2500.0 mm / 2500.0 numérico.
        """
        self.app.valor_var.set("2.5")
        self.app.origen_var.set("m")
        self.app.destino_var.set("mm")

        self.app.solicitar_conversion()

        self.assertEqual(self.app.ultimo_resultado_num, 2500.0)
        self.assertIn("2500.0", self.app.resultado_var.get())

    def test_gui_escenario_limpiar_zona_de_resultado(self):
        """Escenario: Limpiar la zona de resultado
        Dado que existe un resultado de conversión "100 cm"
        Cuando el usuario presiona el botón de limpiar
        Entonces la zona de resultado debe quedar vacía
        """
        # Dado que existe un resultado de conversión "100 cm"
        self.app.resultado_var.set("100 cm")
        self.assertEqual(self.app.resultado_var.get(), "100 cm")

        # Cuando el usuario presiona el botón de limpiar
        self.app.limpiar_resultado()

        # Entonces la zona de resultado debe quedar vacía
        self.assertEqual(self.app.resultado_var.get(), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)

