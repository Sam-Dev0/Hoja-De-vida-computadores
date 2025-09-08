import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect("computadores.db")
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute("""
    CREATE TABLE IF NOT EXISTS computadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        serie TEXT,
        fecha_ingreso TEXT,
        mantenimiento TEXT,
        fecha_mantenimiento TEXT,
        tecnico TEXT,
        descripcion TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_computador INTEGER,
        fecha TEXT,
        tipo TEXT,
        descripcion TEXT,
        FOREIGN KEY (id_computador) REFERENCES computadores(id)
    )
""")
conn.commit()

computador_actual_id = None

def guardar_computador():
    nombre = entry_nombre.get()
    serial = entry_serie.get()
    fecha_ingreso = entry_fecha_ingreso.get()
    mantenimiento = entry_mantenimiento.get()
    fecha_mantenimiento = entry_fecha_mantenimiento.get()
    tecnico = entry_tecnico.get()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()

    cursor.execute("""
        INSERT INTO computadores (nombre, serie, fecha_ingreso, mantenimiento, fecha_mantenimiento, tecnico, descripcion)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (nombre, serial, fecha_ingreso, mantenimiento, fecha_mantenimiento, tecnico, descripcion))
    conn.commit()
    messagebox.showinfo("Éxito", "Computador guardado correctamente.")
    limpiar_campos()

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_serie.delete(0, tk.END)
    entry_fecha_ingreso.delete(0, tk.END)
    entry_mantenimiento.delete(0, tk.END)
    entry_fecha_mantenimiento.delete(0, tk.END)
    entry_tecnico.delete(0, tk.END)
    entry_busqueda.delete(0, tk.END)
    entry_descripcion.delete("1.0", tk.END)
    resultado_historial.delete("1.0", tk.END)

def buscar_computador():
    global computador_actual_id
    termino = entry_busqueda.get()
    cursor.execute("SELECT * FROM computadores WHERE nombre LIKE ? OR serie LIKE ? OR id = ?", 
                   ('%' + termino + '%', '%' + termino + '%', termino))
    resultado = cursor.fetchone()
    if resultado:
        mostrar_resultado(resultado)
        computador_actual_id = resultado[0]
        mostrar_historial(computador_actual_id)
    else:
        messagebox.showinfo("Sin resultados", "No se encontró el computador.")

def mostrar_resultado(fila):
    limpiar_campos()
    entry_nombre.insert(0, fila[1])
    entry_serie.insert(0, fila[2])
    entry_fecha_ingreso.insert(0, fila[3])
    entry_mantenimiento.insert(0, fila[4])
    entry_fecha_mantenimiento.insert(0, fila[5])
    entry_tecnico.insert(0, fila[6])
    entry_descripcion.insert("1.0", fila[7])

def actualizar_computador():
    global computador_actual_id
    if computador_actual_id is None:
        messagebox.showwarning("Error", "Primero debes buscar un computador.")
        return

    nombre = entry_nombre.get()
    serial = entry_serie.get()
    fecha_ingreso = entry_fecha_ingreso.get()
    mantenimiento = entry_mantenimiento.get()
    fecha_mantenimiento = entry_fecha_mantenimiento.get()
    tecnico = entry_tecnico.get()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()

    cursor.execute("""
        UPDATE computadores
        SET nombre=?, serie=?, fecha_ingreso=?, mantenimiento=?, fecha_mantenimiento=?, tecnico=?, descripcion=?
        WHERE id=?""",
        (nombre, serial, fecha_ingreso, mantenimiento, fecha_mantenimiento, tecnico, descripcion, computador_actual_id))
    conn.commit()

    agregar_a_historial(computador_actual_id, fecha_mantenimiento, mantenimiento, descripcion)
    messagebox.showinfo("Éxito", "Computador actualizado y guardado en historial.")
    mostrar_historial(computador_actual_id)

def agregar_a_historial(id_compu, fecha, tipo, descripcion):
    cursor.execute("""
        INSERT INTO historial (id_computador, fecha, tipo, descripcion)
        VALUES (?, ?, ?, ?)""", (id_compu, fecha, tipo, descripcion))
    conn.commit()

def mostrar_historial(id_compu):
    cursor.execute("SELECT fecha, tipo, descripcion FROM historial WHERE id_computador = ?", (id_compu,))
    historial = cursor.fetchall()

    resultado_historial.delete("1.0", tk.END)
    if historial:
        historial_texto = f"Historial del computador (ID: {id_compu}):\n\n"
        for fila in historial:
            historial_texto += f"- Fecha: {fila[0]} | Tipo: {fila[1]} | Descripción: {fila[2]}\n"
    else:
        historial_texto = f"No hay historial registrado para el computador (ID: {id_compu})"
    resultado_historial.insert(tk.END, historial_texto)

# Crear ventana
ventana = tk.Tk()
ventana.title("Hoja de vida de computadores y mantenimiento")
ventana.configure(bg="#e6f2ff")
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=3)
for i in range(11):
    ventana.rowconfigure(i, weight=1)

# Estilo
estilo_labels = {"bg": "#e6f2ff", "fg": "#003366", "font": ("Arial", 10, "bold")}
estilo_botones = {"bg": "#004080", "fg": "white", "font": ("Arial", 10, "bold")}
estilo_entry = {"bg": "white"}

# Campos
tk.Label(ventana, text="Nombre:", **estilo_labels).grid(row=0, column=0, sticky="e", padx=5, pady=2)
entry_nombre = tk.Entry(ventana, **estilo_entry)
entry_nombre.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

tk.Label(ventana, text="Serial:", **estilo_labels).grid(row=1, column=0, sticky="e", padx=5, pady=2)
entry_serie = tk.Entry(ventana, **estilo_entry)
entry_serie.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

tk.Label(ventana, text="Fecha ingreso:", **estilo_labels).grid(row=2, column=0, sticky="e", padx=5, pady=2)
entry_fecha_ingreso = tk.Entry(ventana, **estilo_entry)
entry_fecha_ingreso.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

tk.Label(ventana, text="Tipo mantenimiento:", **estilo_labels).grid(row=3, column=0, sticky="e", padx=5, pady=2)
entry_mantenimiento = tk.Entry(ventana, **estilo_entry)
entry_mantenimiento.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

tk.Label(ventana, text="Fecha mantenimiento:", **estilo_labels).grid(row=4, column=0, sticky="e", padx=5, pady=2)
entry_fecha_mantenimiento = tk.Entry(ventana, **estilo_entry)
entry_fecha_mantenimiento.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

tk.Label(ventana, text="Técnico:", **estilo_labels).grid(row=5, column=0, sticky="e", padx=5, pady=2)
entry_tecnico = tk.Entry(ventana, **estilo_entry)
entry_tecnico.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

tk.Label(ventana, text="Descripción:", **estilo_labels).grid(row=6, column=0, sticky="ne", padx=5, pady=2)
entry_descripcion = tk.Text(ventana, height=4, bg="white")
entry_descripcion.grid(row=6, column=1, sticky="nsew", padx=5, pady=2)

# Botones
btn_guardar = tk.Button(ventana, text="Guardar", command=guardar_computador, **estilo_botones)
btn_guardar.grid(row=7, column=0, columnspan=2, pady=5, sticky="ew", padx=40)

btn_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_computador, **estilo_botones)
btn_actualizar.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew", padx=40)

# Búsqueda
tk.Label(ventana, text="Buscar por nombre, serie o ID:", **estilo_labels).grid(row=9, column=0, sticky="e", padx=5, pady=2)
entry_busqueda = tk.Entry(ventana, **estilo_entry)
entry_busqueda.grid(row=9, column=1, sticky="ew", padx=5, pady=2)

btn_buscar = tk.Button(ventana, text="Buscar", command=buscar_computador, **estilo_botones)
btn_buscar.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew", padx=40)

# Cuadro de historial
resultado_historial = tk.Text(ventana, height=10, wrap="word", bg="white")
resultado_historial.grid(row=11, column=0, columnspan=2, pady=10, padx=5, sticky="nsew")
ventana.mainloop()
