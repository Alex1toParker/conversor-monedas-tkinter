import tkinter as tk
from tkinter import messagebox, ttk
import requests
import csv
from datetime import datetime

MONEDAS = [
    "USD", "EUR", "GBP", "JPY", "MXN", "COP", "ARS", "BRL", "CLP", "CAD",
    "AUD", "CHF", "CNY", "INR", "RUB", "KRW", "ZAR"
]

HISTORIAL_FILE = "historial_conversiones.csv"

def obtener_tasa(base, destino):
    url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"
    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        raise Exception("Error al consultar la API")
    datos = respuesta.json()
    tasa = datos["rates"].get(destino.upper())
    if tasa is None:
        raise ValueError("Moneda destino no válida")
    return tasa, datos["date"]

def guardar_en_historial(base, destino, cantidad, resultado, fecha):
    with open(HISTORIAL_FILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), base, destino, cantidad, resultado, fecha])

def convertir():
    base = combo_base.get()
    destino = combo_destino.get()
    cantidad_str = entry_cantidad.get()
    try:
        if not base or not destino:
            raise ValueError("Seleccione ambas monedas")
        cantidad = float(cantidad_str)
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a cero")
        tasa, fecha = obtener_tasa(base, destino)
        resultado = cantidad * tasa
        label_resultado.config(
            text=f"{cantidad} {base} = {round(resultado, 2)} {destino}"
        )
        label_fecha.config(text=f"Actualizado: {fecha}")
        guardar_en_historial(base, destino, cantidad, round(resultado, 2), fecha)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def limpiar():
    combo_base.set('')
    combo_destino.set('')
    entry_cantidad.delete(0, tk.END)
    label_resultado.config(text="")
    label_fecha.config(text="")

def cambiar_tema():
    global tema_oscuro
    tema_oscuro = not tema_oscuro
    if tema_oscuro:
        colores = {"bg": "#222", "fg": "#fff", "entry_bg": "#333", "entry_fg": "#fff"}
        btn_tema.config(text="Tema Claro")
    else:
        colores = {"bg": "#f0f0f0", "fg": "#000", "entry_bg": "#fff", "entry_fg": "#000"}
        btn_tema.config(text="Tema Oscuro")
    ventana.config(bg=colores["bg"])
    for widget in ventana.winfo_children():
        if isinstance(widget, (tk.Label, ttk.Combobox, tk.Button)):
            widget.config(bg=colores["bg"], fg=colores["fg"])
        if isinstance(widget, tk.Entry):
            widget.config(bg=colores["entry_bg"], fg=colores["entry_fg"])

ventana = tk.Tk()
ventana.title("Conversor de Monedas")
ventana.geometry("400x320")
ventana.resizable(False, False)

tema_oscuro = False

tk.Label(ventana, text="Moneda Base:").pack(pady=5)
combo_base = ttk.Combobox(ventana, values=MONEDAS, state="readonly")
combo_base.pack()

tk.Label(ventana, text="Moneda Destino:").pack(pady=5)
combo_destino = ttk.Combobox(ventana, values=MONEDAS, state="readonly")
combo_destino.pack()

tk.Label(ventana, text="Cantidad:").pack(pady=5)
entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()

tk.Button(ventana, text="Convertir", command=convertir).pack(pady=10)
tk.Button(ventana, text="Limpiar", command=limpiar).pack(pady=2)

label_resultado = tk.Label(ventana, text="", font=("Helvetica", 12, "bold"))
label_resultado.pack(pady=5)

label_fecha = tk.Label(ventana, text="", font=("Helvetica", 9))
label_fecha.pack(pady=2)

btn_tema = tk.Button(ventana, text="Tema Oscuro", command=cambiar_tema)
btn_tema.pack(pady=5)

ventana.mainloop()