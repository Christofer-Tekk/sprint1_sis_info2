from tkinter import messagebox
from conexion import conectar
import tkinter as tk

def pantalla_registrar(contenedor, volver):

    # -------------------------
    # LIMPIAR CONTENEDOR
    # -------------------------
    for widget in contenedor.winfo_children():
        widget.destroy()

    # -------------------------
    # UI
    # -------------------------
    tk.Label(contenedor, text="Registrar Paciente",
             font=("Arial", 18, "bold"),
             bg="#E3F2FD").pack(pady=15)

    # Nombre
    tk.Label(contenedor, text="Nombre", bg="#E3F2FD").pack()
    entry_nombre = tk.Entry(contenedor)
    entry_nombre.pack(pady=5)

    # CI
    tk.Label(contenedor, text="CI", bg="#E3F2FD").pack()
    entry_ci = tk.Entry(contenedor)
    entry_ci.pack(pady=5)

    # Teléfono
    tk.Label(contenedor, text="Teléfono", bg="#E3F2FD").pack()
    entry_tel = tk.Entry(contenedor)
    entry_tel.pack(pady=5)

    # -------------------------
    # VALIDAR SOLO NÚMEROS
    # -------------------------
    def solo_numeros(texto):
        return texto.isdigit() or texto == ""

    validar = contenedor.register(solo_numeros)

    entry_ci.config(validate="key", validatecommand=(validar, "%P"))
    entry_tel.config(validate="key", validatecommand=(validar, "%P"))

    # -------------------------
    # GUARDAR
    # -------------------------
    def guardar():
        nombre = entry_nombre.get().strip()
        ci = entry_ci.get().strip()
        tel = entry_tel.get().strip()

        # -------------------------
        # VALIDACIONES
        # -------------------------
        if nombre == "" or ci == "":
            messagebox.showerror("Error", "Nombre y CI son obligatorios")
            return

        # CI: 5 a 10 dígitos
        if len(ci) < 5 or len(ci) > 10:
            messagebox.showerror("Error", "CI debe tener entre 5 y 10 dígitos")
            return

        # Teléfono: 8 dígitos
        if len(tel) != 8:
            messagebox.showerror("Error", "Teléfono debe tener 8 dígitos")
            return

        # Teléfono inicia con 6 o 7
        if not (tel.startswith("6") or tel.startswith("7")):
            messagebox.showerror("Error", "Teléfono debe iniciar con 6 o 7")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO pacientes (nombre, ci, telefono) VALUES (%s, %s, %s)",
                (nombre, ci, tel)
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Paciente registrado correctamente")

            # Limpiar campos
            entry_nombre.delete(0, tk.END)
            entry_ci.delete(0, tk.END)
            entry_tel.delete(0, tk.END)

        except:
            messagebox.showerror("Error", "El CI ya existe")

    # -------------------------
    # BOTONES
    # -------------------------
    tk.Button(contenedor, text="Guardar",
              bg="#1976D2", fg="white",
              width=20, height=2,
              relief="flat",
              command=guardar).pack(pady=15)

    tk.Button(contenedor, text="← Volver",
              command=volver).pack(pady=10)
