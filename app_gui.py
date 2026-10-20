"""Interfaz gráfica de usuario (GUI) con Tkinter para el conversor de medidas de longitud.
Implementa los escenarios BDD definidos para mm, cm y m.
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
        self.root.geometry("460x380")
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
            anchor="center"
        )
        self.lbl_resultado.pack(fill="both", expand=True)

    def solicitar_conversion(self):
        """Ejecuta la conversión con los valores actuales de los campos."""
        texto_valor = self.valor_var.get().strip()
        if not texto_valor:
            messagebox.showwarning("Atención", "Por favor introduzca un valor a convertir.")
            return

        try:
            val = float(texto_valor)
        except ValueError:
            messagebox.showerror("Error", f"El valor '{texto_valor}' no es un número válido.")
            return

        origen = self.origen_var.get()
        destino = self.destino_var.get()

        try:
            res = convertir(val, origen, destino)
            self.ultimo_resultado_num = res
            # Si el resultado es entero en valor flotante, se formatea coherentemente (ej: 50.0, 2500.0)
            self.resultado_var.set(f"{res} {destino}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_resultado(self):
        """Limpia la zona de resultado según la especificación del escenario BDD."""
        self.resultado_var.set("")
        self.ultimo_resultado_num = None

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

