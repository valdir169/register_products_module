"""
Gestor de productos - Tienda piloto Plaza Vea (Supermercados Peruanos S.A.)
Solución 1: arreglos (listas) + funciones + archivo JSON + interfaz Tkinter.
"""
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "productos.json")
UNIDADES = ["kg", "g", "l", "ml", "unidad", "paquete", "caja"]


# ---------------------------------------------------------------
# CAPA DE DATOS (archivo JSON)
# ---------------------------------------------------------------
def cargar_productos():
    """Lee el JSON y devuelve el arreglo de productos."""
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_productos(productos):
    """Guarda el arreglo completo en el JSON."""
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False, indent=4)


# ---------------------------------------------------------------
# CAPA DE LÓGICA (operaciones sobre el arreglo)
# ---------------------------------------------------------------
def buscar_indice(productos, codigo):
    """Recorre el arreglo y devuelve la posición del código, o -1."""
    for i, p in enumerate(productos):
        if p["codigo"].lower() == codigo.lower():
            return i
    return -1


def validar_datos(codigo, descripcion, stock, precio, unidad):
    """Devuelve (producto, None) si es válido, o (None, mensaje_error)."""
    codigo, descripcion = codigo.strip(), descripcion.strip()
    if not codigo or not descripcion:
        return None, "El código y la descripción son obligatorios."
    if not unidad:
        return None, "Seleccione una unidad de medida."
    try:
        stock = int(stock)
        if stock < 0:
            raise ValueError
    except ValueError:
        return None, "El stock debe ser un número entero mayor o igual a 0."
    try:
        precio = float(precio)
        if precio < 0:
            raise ValueError
    except ValueError:
        return None, "El precio debe ser un número mayor o igual a 0."
    return {
        "codigo": codigo.upper(),
        "descripcion": descripcion,
        "stock": stock,
        "precio": round(precio, 2),
        "unidad_medida": unidad,
    }, None


def registrar_producto(productos, nuevo):
    if buscar_indice(productos, nuevo["codigo"]) != -1:
        return False, f"Ya existe un producto con el código {nuevo['codigo']}."
    productos.append(nuevo)
    guardar_productos(productos)
    return True, "Producto registrado correctamente."


def actualizar_producto(productos, datos):
    i = buscar_indice(productos, datos["codigo"])
    if i == -1:
        return False, "El código no existe. Use 'Registrar' para crearlo."
    productos[i] = datos
    guardar_productos(productos)
    return True, "Producto actualizado correctamente."


def consultar_productos(productos, texto=""):
    """Filtra por código o descripción. Sin texto devuelve todo (listar)."""
    texto = texto.strip().lower()
    if not texto:
        return list(productos)
    return [p for p in productos
            if texto in p["codigo"].lower() or texto in p["descripcion"].lower()]


# ---------------------------------------------------------------
# CAPA DE INTERFAZ (Tkinter)
# ---------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Productos - Plaza Vea (Tienda piloto)")
        self.geometry("860x560")
        self.minsize(760, 500)
        self.productos = cargar_productos()

        self.var_codigo = tk.StringVar()
        self.var_desc = tk.StringVar()
        self.var_stock = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_unidad = tk.StringVar()
        self.var_buscar = tk.StringVar()

        self._crear_formulario()
        self._crear_buscador()
        self._crear_tabla()
        self.refrescar_tabla()

    def _crear_formulario(self):
        marco = ttk.LabelFrame(self, text="Datos del producto", padding=10)
        marco.pack(fill="x", padx=12, pady=(12, 6))

        campos = [
            ("Código:", ttk.Entry(marco, textvariable=self.var_codigo, width=14)),
            ("Descripción:", ttk.Entry(marco, textvariable=self.var_desc, width=34)),
            ("Stock:", ttk.Entry(marco, textvariable=self.var_stock, width=10)),
            ("Precio (S/):", ttk.Entry(marco, textvariable=self.var_precio, width=10)),
            ("Unidad:", ttk.Combobox(marco, textvariable=self.var_unidad,
                                     values=UNIDADES, state="readonly", width=12)),
        ]
        self.entry_codigo = campos[0][1]
        posiciones = [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0)]
        for (texto, widget), (f, c) in zip(campos, posiciones):
            ttk.Label(marco, text=texto).grid(row=f, column=c, sticky="e", padx=4, pady=4)
            widget.grid(row=f, column=c + 1, sticky="w", padx=4, pady=4)

        botones = ttk.Frame(marco)
        botones.grid(row=2, column=2, columnspan=2, sticky="e", pady=4)
        ttk.Button(botones, text="Registrar", command=self.on_registrar).pack(side="left", padx=3)
        ttk.Button(botones, text="Actualizar", command=self.on_actualizar).pack(side="left", padx=3)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=3)

    def _crear_buscador(self):
        marco = ttk.Frame(self)
        marco.pack(fill="x", padx=12, pady=6)
        ttk.Label(marco, text="Buscar (código o descripción):").pack(side="left")
        entrada = ttk.Entry(marco, textvariable=self.var_buscar, width=32)
        entrada.pack(side="left", padx=6)
        entrada.bind("<KeyRelease>", lambda e: self.refrescar_tabla())
        ttk.Button(marco, text="Ver todos", command=self.on_ver_todos).pack(side="left")
        self.lbl_total = ttk.Label(marco, text="")
        self.lbl_total.pack(side="right")

    def _crear_tabla(self):
        marco = ttk.Frame(self)
        marco.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        cols = ("codigo", "descripcion", "stock", "precio", "unidad")
        encabezados = ("Código", "Descripción", "Stock", "Precio (S/)", "Unidad")
        anchos = (90, 330, 80, 100, 90)

        self.tabla = ttk.Treeview(marco, columns=cols, show="headings", selectmode="browse")
        for c, h, a in zip(cols, encabezados, anchos):
            self.tabla.heading(c, text=h)
            self.tabla.column(c, width=a, anchor="w" if c == "descripcion" else "center")
        barra = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self.on_seleccionar)

    # --- acciones ---
    def refrescar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        resultado = consultar_productos(self.productos, self.var_buscar.get())
        for p in resultado:
            self.tabla.insert("", "end", values=(
                p["codigo"], p["descripcion"], p["stock"],
                f"{p['precio']:.2f}", p["unidad_medida"]))
        self.lbl_total.config(text=f"Mostrando {len(resultado)} de {len(self.productos)}")

    def _leer_formulario(self):
        return validar_datos(self.var_codigo.get(), self.var_desc.get(),
                             self.var_stock.get(), self.var_precio.get(),
                             self.var_unidad.get())

    def on_registrar(self):
        datos, error = self._leer_formulario()
        if error:
            return messagebox.showwarning("Datos inválidos", error)
        ok, msg = registrar_producto(self.productos, datos)
        (messagebox.showinfo if ok else messagebox.showerror)("Registrar", msg)
        if ok:
            self.limpiar_formulario()
            self.refrescar_tabla()

    def on_actualizar(self):
        datos, error = self._leer_formulario()
        if error:
            return messagebox.showwarning("Datos inválidos", error)
        ok, msg = actualizar_producto(self.productos, datos)
        (messagebox.showinfo if ok else messagebox.showerror)("Actualizar", msg)
        if ok:
            self.limpiar_formulario()
            self.refrescar_tabla()

    def on_seleccionar(self, _evento):
        sel = self.tabla.selection()
        if not sel:
            return
        cod, desc, stock, precio, unidad = self.tabla.item(sel[0])["values"]
        self.var_codigo.set(cod)
        self.var_desc.set(desc)
        self.var_stock.set(stock)
        self.var_precio.set(precio)
        self.var_unidad.set(unidad)

    def on_ver_todos(self):
        self.var_buscar.set("")
        self.refrescar_tabla()

    def limpiar_formulario(self):
        for v in (self.var_codigo, self.var_desc, self.var_stock,
                  self.var_precio, self.var_unidad):
            v.set("")
        self.tabla.selection_remove(self.tabla.selection())
        self.entry_codigo.focus()


if __name__ == "__main__":
    App().mainloop()