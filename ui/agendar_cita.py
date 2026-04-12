import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from conexion import conectar

#paleta de colores
FONDO = "#E3F2FD"
AZUL = "#1976D2"
VERDE = "#4CAF50"
ROJO = "#E53935"

def pantalla_agendar(contenedor, volver):
     # Limpiar contenedor
    for widget in contenedor.winfo_children():
        widget.destroy()

    def agendar_cita():
        paciente = entry_paciente.get()
        fecha = entry_fecha.get()
        medico = combo_medico.get()

        if paciente == "" or fecha == "" or medico == "":
            messagebox.showerror("Error", "Por favor completa todos los campos")
        else:
            messagebox.showinfo("Éxito", f"Cita agendada para {paciente}")
            entry_paciente.delete(0, tk.END)
            entry_fecha.delete(0, tk.END)
            combo_medico.set("")

    # Frame principal (tarjeta centrada)
    frame = tk.Frame(contenedor, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=420)

    # Título
    tk.Label(frame, text="Agendar Cita",
             bg="white", fg=AZUL,
             font=("Helvetica", 18, "bold")).pack(pady=20)

    # Nombre paciente
    tk.Label(frame, text="Nombre y Apellido", bg="white").pack(anchor="w", padx=40)
    entry_paciente = tk.Entry(frame, bd=2, relief="flat")
    entry_paciente.pack(padx=40, pady=5, fill="x")

# CI

    tk.Label(frame, text="CI del paciente", bg="white").pack(anchor="w", padx=40)
    entry_ci = tk.Entry(frame)
    entry_ci.pack(padx=40, pady=5, fill="x")

    # Fecha
    tk.Label(frame, text="Fecha (dd/mm/aaaa)", bg="white").pack(anchor="w", padx=40)
    entry_fecha = DateEntry(frame, width=18, background="#1976D2", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd"
    )
    entry_fecha.pack(padx=40, pady=5, fill="x")

    # Médico
    tk.Label(frame, text="Seleccionar médico", bg="white").pack(anchor="w", padx=40)
    combo_medico = ttk.Combobox(frame, values=[
        "Dr. Pérez", "Dra. Gómez", "Dr. López"
    ])
    combo_medico.pack(padx=40, pady=5, fill="x")

    # Botón agendar
    tk.Button(frame, text="Agendar Cita",
              bg=VERDE, fg="white",
              font=("Helvetica", 12, "bold"),
              relief="flat",
              command=agendar_cita).pack(pady=20, ipadx=10, ipady=5)

    # botón volver
    tk.Button(frame, text="← Volver",
              bg=ROJO, fg="white",
              font=("Helvetica", 10),
              relief="flat",
              command=volver).pack()
