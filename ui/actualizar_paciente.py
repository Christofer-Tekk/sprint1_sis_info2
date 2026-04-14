import tkinter as tk
from tkinter import messagebox
from conexion import conectar

def pantalla_actualizar(contenedor, volver):

    # ── Limpiar contenedor (patrón del equipo) ───────────────
    for widget in contenedor.winfo_children():
        widget.destroy()

    # ── Título ───────────────────────────────────────────────
    tk.Label(contenedor, text="Actualizar Paciente",
             font=("Arial", 18, "bold"),
             bg="#E3F2FD", fg="#1976D2").pack(pady=15)

    # ── Campo CI para buscar ─────────────────────────────────
    tk.Label(contenedor, text="CI del Paciente:",
             bg="#E3F2FD", font=("Arial", 11)).pack()
    entry_ci = tk.Entry(contenedor, font=("Arial", 11),
                        width=25, justify="center")
    entry_ci.pack(pady=5)

    # ── Frame edición (oculto al inicio) ─────────────────────
    frame_edicion = tk.Frame(contenedor, bg="#E3F2FD")

    tk.Label(frame_edicion, text="Nombre:",
             bg="#E3F2FD", font=("Arial", 11)).pack()
    entry_nombre = tk.Entry(frame_edicion, font=("Arial", 11),
                            width=25, justify="center")
    entry_nombre.pack(pady=5)

    tk.Label(frame_edicion, text="Teléfono:",
             bg="#E3F2FD", font=("Arial", 11)).pack()
    entry_telefono = tk.Entry(frame_edicion, font=("Arial", 11),
                              width=25, justify="center")
    entry_telefono.pack(pady=5)

    # ============================================================
    # TASK 1 y 2 — Buscar y precargar datos
    # ============================================================
    def buscar_paciente():
        ci = entry_ci.get().strip()

        if not ci:
            messagebox.showwarning("Campo vacío",
                                   "Por favor ingresa un CI.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM pacientes WHERE ci = %s", (ci,))
            resultado = cursor.fetchone()
            conn.close()

            # TASK 1 — ¿Existe?
            if resultado is None:
                messagebox.showerror("No encontrado",
                                     "No existe un paciente con ese CI.")
                frame_edicion.pack_forget()
                return

            # TASK 2 — Precargar datos
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, resultado[1] if resultado[1] else "")    # nombre
            entry_telefono.delete(0, tk.END)
            entry_telefono.insert(0, resultado[3] if resultado[3] else "")  # telefono
            frame_edicion.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))

    # ============================================================
    # TASK 3 y 4 — Validar y Guardar
    # ============================================================
    def guardar_cambios():
        ci       = entry_ci.get().strip()
        nombre   = entry_nombre.get().strip()
        telefono = entry_telefono.get().strip()

        # TASK 3 — Validaciones
        if not nombre:
            messagebox.showwarning("Campo vacío",
                                   "El nombre no puede estar vacío.")
            return

        if len(telefono) != 8:
            messagebox.showwarning("Teléfono inválido",
                           "El teléfono debe tener exactamente 8 dígitos.")
            return

        if not telefono.isdigit():
            messagebox.showwarning("Teléfono inválido",
                                   "El teléfono solo debe contener números.")
            return  

        if telefono[0] not in ("6", "7"):
            messagebox.showwarning("Teléfono inválido",
                                   "El teléfono debe iniciar con 6 o 7.")
            return

        try:
            # TASK 4 — Guardar en BD
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE pacientes SET nombre=%s, telefono=%s WHERE ci=%s",
                (nombre, telefono, ci)
            )
            conn.commit()
            conn.close()

            # TASK 5 — Confirmación
            messagebox.showinfo("✅ Éxito",
                                "Datos actualizados correctamente.")
            frame_edicion.pack_forget()
            entry_ci.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ── Botón Buscar ─────────────────────────────────────────
    tk.Button(contenedor, text="Buscar",
              bg="#1976D2", fg="white",
              font=("Arial", 11, "bold"),
              width=20, height=2,
              command=buscar_paciente).pack(pady=8)

    # ── Botón Guardar (dentro del frame) ─────────────────────
    tk.Button(frame_edicion, text="💾 Guardar Cambios",
              bg="#4CAF50", fg="white",
              font=("Arial", 11, "bold"),
              width=20, height=2,
              command=guardar_cambios).pack(pady=10)

    # ── Botón Volver ─────────────────────────────────────────
    tk.Button(contenedor, text="← Volver",
              bg="#E53935", fg="white",
              font=("Arial", 10),
              width=20,
              command=volver).pack(pady=5)