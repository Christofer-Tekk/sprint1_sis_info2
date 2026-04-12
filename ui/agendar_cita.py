import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from conexion import conectar

FONDO = "#E3F2FD"
AZUL = "#1976D2"
VERDE = "#4CAF50"
ROJO = "#E53935"

def pantalla_agendar(contenedor, volver):

    # LIMPIAR
    for widget in contenedor.winfo_children():
        widget.destroy()

    # -------------------------
    # FUNCIÓN INTERNA
    # -------------------------
    def agendar_cita():
        nombre = entry_paciente.get()
        ci = entry_ci.get()
        fecha = entry_fecha.get()
        medico = combo_medico.get()

        if nombre == "" or ci == "" or fecha == "" or medico == "":
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("SELECT id FROM pacientes WHERE ci = %s", (ci,))
            resultado = cursor.fetchone()

            if resultado:
                paciente_id = resultado[0]
            else:
                cursor.execute(
                    "INSERT INTO pacientes (nombre, ci) VALUES (%s, %s)",
                    (nombre, ci)
                )
                conexion.commit()
                paciente_id = cursor.lastrowid

            sql = """
            INSERT INTO citas (paciente_id, medico, fecha, hora, estado)
            VALUES (%s, %s, %s, %s, %s)
            """

            valores = (paciente_id, medico, fecha, "10:00:00", "Activa")

            cursor.execute(sql, valores)
            conexion.commit()

            messagebox.showinfo("Éxito", "¡Cita guardada correctamente!")

            entry_paciente.delete(0, tk.END)
            entry_ci.delete(0, tk.END)
            combo_medico.set("")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        finally:
            cursor.close()
            conexion.close()

    # -------------------------
    # INTERFAZ
    # -------------------------
    frame = tk.Frame(contenedor, bg="white")
    frame.pack(expand=True)

    tk.Label(frame, text="Agendar Cita",
             bg="white", fg=AZUL,
             font=("Helvetica", 18, "bold")).pack(pady=20)

    tk.Label(frame, text="Nombre y Apellido", bg="white").pack(anchor="w", padx=40)
    entry_paciente = tk.Entry(frame)
    entry_paciente.pack(padx=40, pady=5, fill="x")

    tk.Label(frame, text="CI del paciente", bg="white").pack(anchor="w", padx=40)
    entry_ci = tk.Entry(frame)
    entry_ci.pack(padx=40, pady=5, fill="x")

    tk.Label(frame, text="Fecha", bg="white").pack(anchor="w", padx=40)
    entry_fecha = DateEntry(frame, date_pattern="yyyy-mm-dd")
    entry_fecha.pack(padx=40, pady=5, fill="x")

    tk.Label(frame, text="Seleccionar médico", bg="white").pack(anchor="w", padx=40)
    combo_medico = ttk.Combobox(frame, values=[
        "Dr. Pérez", "Dra. Gómez", "Dr. López"
    ])
    combo_medico.pack(padx=40, pady=5, fill="x")

    tk.Button(frame, text="Agendar Cita",
              bg=VERDE, fg="white",
              command=agendar_cita).pack(pady=20)

    tk.Button(frame, text="← Volver",
              bg=ROJO, fg="white",
              command=volver).pack()