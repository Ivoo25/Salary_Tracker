import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
from ttkthemes import themed_tk as ttkh

# Cargar el archivo Excel
try:
    df = pd.read_excel("gastos.xlsx")
except:
    # Si el archivo no existe, crear un nuevo DataFrame
    df = pd.DataFrame(columns=["Fecha", "Gasto", "Monto"])

# Función para actualizar la lista de gastos
def actualizar_gastos():
    # Limpiar la lista de gastos
    lista_gastos.delete(0, tk.END)
    # Obtener la lista de gastos únicos
    gastos_unicos = df["Gasto"].unique()
    # Agregar cada gasto único a la lista de gastos
    for gasto in gastos_unicos:
        lista_gastos.insert(tk.END, gasto)

# Función para agregar un gasto
def agregar_gasto():
    # Obtener la opción seleccionada
    seleccion = lista_opciones.get()
    # Obtener el monto ingresado
    monto = float(entry_monto.get())
    # Crear una nueva fila con la fecha actual, la opción seleccionada y el monto ingresado
    nueva_fila = {"Fecha": datetime.now(), "Gasto": seleccion, "Monto": monto}
    # Agregar la nueva fila al DataFrame
    df = df.append(nueva_fila, ignore_index=True)
    # Guardar el DataFrame en el archivo Excel
    df.to_excel("gastos.xlsx", index=False)
    # Actualizar la lista de gastos
    actualizar_gastos()
    # Limpiar el campo del monto
    entry_monto.delete(0, tk.END)

# Función para restar un valor
def restar_valor():
    # Obtener la opción seleccionada
    seleccion = lista_gastos.get(tk.ACTIVE)
    # Obtener el monto ingresado
    monto = float(entry_monto.get())
    # Obtener el índice de la fila correspondiente al gasto seleccionado
    indice = df[df["Gasto"] == seleccion].index[0]
    # Restar el monto ingresado al monto correspondiente en el DataFrame
    df.at[indice, "Monto"] -= monto
    # Guardar el DataFrame en el archivo Excel
    df.to_excel("gastos.xlsx", index=False)
    # Actualizar la lista de gastos
    actualizar_gastos()
    # Limpiar el campo del monto
    entry_monto.delete(0, tk.END)

# Función para resetear el saldo
def resetear_saldo():
    # Obtener el saldo actual
    saldo_actual = sum(df["Monto"])
    # Crear una nueva fila con la fecha actual, la opción "Ahorros" y el saldo actual
    nueva_fila = {"Fecha": datetime.now(), "Gasto": "Ahorros", "Monto": saldo_actual}
    # Agregar la nueva fila al DataFrame
    df = df.append(nueva_fila, ignore_index=True)
    # Eliminar todas las filas del DataFrame excepto la última (que corresponde a los ahorros)
    df = df.iloc[[-1]]
    # Guardar el DataFrame en el archivo Excel
    df.to_excel("gastos.xlsx", index=False)
    # Actualizar la lista de gastos
    actualizar_gastos()

# Función para ingresar el saldo inicial
def ingresar_saldo():
    saldo = float(entry_saldo.get())
    if saldo >= 0:
        global saldo_actual
        saldo_actual = saldo
        actualizar_saldo()
        entry_saldo.delete(0, tk.END)
        entry_saldo.config(state=tk.DISABLED)
        boton_saldo.config(state=tk.DISABLED)
        boton_resetear.config(state=tk.NORMAL)
        boton_agregar.config(state=tk.NORMAL)
        lista_gastos.config(state=tk.NORMAL)
        messagebox.showinfo("Gestor de Sueldo", "Saldo ingresado correctamente.")
    else:
        messagebox.showerror("Error", "El saldo ingresado no es válido.")

    

# Configurar el estilo de la ventana
ventana = ttkh.ThemedTk()
ventana.get_themes()
ventana.set_theme("equilux")

# Configurar la geometría de la ventana
ventana.geometry("400x400")
ventana.title("Gestor de Sueldo")

# Etiqueta del saldo actual
label_saldo_actual = tk.Label(ventana, text="Saldo actual:")
label_saldo_actual.pack(pady=10)

# Etiqueta para mostrar el saldo actual
saldo_actual = sum(df["Monto"])
label_saldo = tk.Label(ventana, text=saldo_actual)
label_saldo.pack()

# Etiqueta de la lista de gastos
label_gastos = tk.Label(ventana, text="Gastos:")
label_gastos.pack(pady=10)

# Lista de gastos
lista_gastos = tk.Listbox(ventana)
lista_gastos.pack(pady=5)

# Etiqueta de la opción a restar
label_opcion = tk.Label(ventana, text="Opción:")
label_opcion.pack()

# Lista de opciones
opciones = ["Alquiler departamento", "Gastos del departamento", "Comida", "Gimnasio", "Salidas"]
lista_opciones = ttk.Combobox(ventana, values=opciones)
lista_opciones.pack()

# Etiqueta del monto a restar
label_monto = tk.Label(ventana, text="Monto:")
label_monto.pack()

# Campo de entrada del monto
entry_monto = ttk.Entry(ventana)
entry_monto.pack()

# Botón para agregar un gasto
boton_agregar = ttk.Button(ventana, text="Agregar Gasto", command=agregar_gasto)
boton_agregar.pack(pady=5)

# Botón para restar un valor
boton_restar = ttk.Button(ventana, text="Restar Valor", command=restar_valor)
boton_restar.pack(pady=5)

# Botón para resetear el saldo
boton_resetear = ttk.Button(ventana, text="Resetear Saldo", command=resetear_saldo)
boton_resetear.pack(pady=5)

# Actualizar la lista de gastos
actualizar_gastos()

# Ejecutar la ventana
ventana.mainloop()
