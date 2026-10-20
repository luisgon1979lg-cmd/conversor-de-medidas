"""Interfaz gráfica de usuario (GUI) con Tkinter para el conversor de medidas de longitud.
Implementa los escenarios BDD definidos para mm, cm y m, y maneja de forma robusta entradas no numéricas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from conversor import convertir, UNIDADES_VALIDAS


class ConversorApp:
    def __init__(self, root: tk.Tk | None = None):
        if root is None:
            self.root = tk.Tk()
            self._owns_root = True
        else:
            self.root = root
            self._owns_root = False

        self.root.title("Conversor de Medidas - Robots Móviles Autónomos")
        self.root.geometry("480x400")
        self.root.resizable(False, False)

        # Variables de estado
        self.valor_var = tk.StringVar(value="")
        self.origen_var = tk.StringVar(value="mm")
        self.destino_var = tk.StringVar(value="cm")
        self.resultado_var = tk.StringVar(value="")
        self.ultimo_resultado_num = None

        self._configurar_estilos()
        self._construir_ui()

    def _configurar_estilos(self):
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground="#1e293b")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 9), foreground="#64748b")
        style.configure("Result.TLabel", font=("Segoe UI", 16, "bold"), foreground="#0284c7")
        style.configure("ErrorResult.TLabel", font=("Segoe UI", 12, "bold"), foreground="#dc2626")
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Secondary.TButton", font=("Segoe UI", 10))

    def _construir_ui(self):
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        # Encabezado
        ttk.Label(
            container,
            text="Conversor de Longitud",
            style="Title.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            container,
            text="Unidades soportadas: mm, cm, m",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(0, 15))

        # Panel de entrada
        form_frame = ttk.LabelFrame(container, text=" Parámetros de conversión ", padding=12)
        form_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(form_frame, text="Valor a convertir:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_valor = ttk.Entry(form_frame, textvariable=self.valor_var, font=("Segoe UI", 10), width=18)
        self.entry_valor.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Unidad de origen:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_origen = ttk.Combobox(
            form_frame,
            textvariable=self.origen_var,
            values=UNIDADES_VALIDAS,
            state="readonly",
            width=10
        )
        self.combo_origen.grid(row=1, column=1, sticky="w", pady=5, padx=5)

        ttk.Label(form_frame, text="Unidad de destino:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_destino = ttk.Combobox(
            form_frame,
            textvariable=self.destino_var,
            values=UNIDADES_VALIDAS,
            state="readonly",
            width=10
        )
        self.combo_destino.grid(row=2, column=1, sticky="w", pady=5, padx=5)

        # Botones de acción
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=(0, 15))

        self.btn_convertir = ttk.Button(
            btn_frame,
            text="Convertir",
            style="Primary.TButton",
            command=self.solicitar_conversion
        )
        self.btn_convertir.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_limpiar = ttk.Button(
            btn_frame,
            text="Limpiar",
            style="Secondary.TButton",
            command=self.limpiar_resultado
        )
        self.btn_limpiar.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # Zona de resultado
        res_frame = ttk.LabelFrame(container, text=" Resultado ", padding=12)
        res_frame.pack(fill="both", expand=True)

        self.lbl_resultado = ttk.Label(
            res_frame,
            textvariable=self.resultado_var,
            style="Result.TLabel",
            anchor="center",
            wraplength=400
        )
        self.lbl_resultado.pack(fill="both", expand=True)

    def solicitar_conversion(self):
        """Ejecuta la conversión con los valores actuales de los campos."""
        texto_valor = self.valor_var.get().strip()
        if not texto_valor:
            self.lbl_resultado.configure(style="ErrorResult.TLabel")
            self.resultado_var.set("Atención: Introduzca un valor a convertir")
            self.ultimo_resultado_num = None
            return

        origen = self.origen_var.get()
        destino = self.destino_var.get()

        try:
            res = convertir(texto_valor, origen, destino)
            self.ultimo_resultado_num = res
            self.lbl_resultado.configure(style="Result.TLabel")
            self.resultado_var.set(f"{res} {destino}")
        except ValueError as e:
            self.ultimo_resultado_num = None
            self.lbl_resultado.configure(style="ErrorResult.TLabel")
            self.resultado_var.set(f"Error: {e}")

    def limpiar_resultado(self):
        """Limpia la zona de resultado según la especificación del escenario BDD."""
        self.resultado_var.set("")
        self.ultimo_resultado_num = None
        self.lbl_resultado.configure(style="Result.TLabel")

    def limpiar_todo(self):
        """Limpia tanto la zona de resultado como el campo de valor."""
        self.limpiar_resultado()
        self.valor_var.set("")

    def mainloop(self):
        if self._owns_root:
            self.root.mainloop()


if __name__ == "__main__":
    app = ConversorApp()
    app.mainloop()
