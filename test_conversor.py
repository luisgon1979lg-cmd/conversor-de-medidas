"""Pruebas automatizadas (BDD / Unit Tests) para el conversor de medidas de longitud.
Reproduce con exactitud los escenarios especificados en el requerimiento Gherkin:
- Conversión de milímetros a centímetros (500 mm -> 50.0 cm)
- Conversión de metros a milímetros (2.5 m -> 2500.0 mm)
- Limpieza de la zona de resultado
- Validación y control de errores al introducir texto/letras (Issue #1: "Explotó")
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

    def test_soporte_coma_decimal(self):
        """Verifica que números con coma decimal (formato estándar en español) sean válidos."""
        self.assertEqual(convertir("2,5", "m", "mm"), 2500.0)
        self.assertEqual(convertir("50,5", "cm", "mm"), 505.0)

    def test_otras_conversiones_validas(self):
        """Pruebas adicionales de cobertura entre todas las combinaciones mm, cm y m."""
        self.assertEqual(convertir(100, "cm", "m"), 1.0)
        self.assertEqual(convertir(1, "m", "cm"), 100.0)
        self.assertEqual(convertir(10, "mm", "mm"), 10.0)
        self.assertEqual(convertir(1500, "mm", "m"), 1.5)

    def test_errores_en_unidades_o_valores_invalidos(self):
        """Validación de manejo de errores al introducir letras o unidades inexistentes."""
        # Introducir letras en vez de números no debe causar un crash no controlado
        with self.assertRaises(ValueError) as ctx:
            convertir("abc", "mm", "cm")
        self.assertIn("no es un número válido", str(ctx.exception))

        with self.assertRaises(ValueError):
            convertir(10, "km", "m")
        with self.assertRaises(ValueError):
            convertir(10, "m", "yardas")


class TestConversorGUI(unittest.TestCase):
    """Pruebas de integración sobre la interfaz gráfica que reproducen la interacción del usuario."""

    @classmethod
    def setUpClass(cls):
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
        self.app.valor_var.set("500")
        self.app.origen_var.set("mm")
        self.app.destino_var.set("cm")

        self.app.solicitar_conversion()

        self.assertEqual(self.app.ultimo_resultado_num, 50.0)
        self.assertIn("50.0", self.app.resultado_var.get())

    def test_gui_escenario_convertir_metros_a_milimetros(self):
        self.app.valor_var.set("2.5")
        self.app.origen_var.set("m")
        self.app.destino_var.set("mm")

        self.app.solicitar_conversion()

        self.assertEqual(self.app.ultimo_resultado_num, 2500.0)
        self.assertIn("2500.0", self.app.resultado_var.get())

    def test_gui_escenario_limpiar_zona_de_resultado(self):
        self.app.resultado_var.set("100 cm")
        self.assertEqual(self.app.resultado_var.get(), "100 cm")

        self.app.limpiar_resultado()

        self.assertEqual(self.app.resultado_var.get(), "")

    def test_gui_manejo_de_letras_sin_explotar(self):
        """Reproduce y soluciona el Issue #1 ('le meto letras y explota'):
        Al meter letras, la interfaz muestra el error amigablemente en pantalla sin colapsar.
        """
        self.app.valor_var.set("hola mundo")
        self.app.origen_var.set("mm")
        self.app.destino_var.set("cm")

        # No debe lanzar excepción no controlada
        self.app.solicitar_conversion()

        # El resultado numérico es None y en la zona de resultado se indica el error
        self.assertIsNone(self.app.ultimo_resultado_num)
        self.assertIn("Error", self.app.resultado_var.get())
        self.assertIn("no es un número válido", self.app.resultado_var.get())


if __name__ == "__main__":
    unittest.main(verbosity=2)
