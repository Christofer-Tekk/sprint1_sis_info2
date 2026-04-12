import tkinter as tk
from ui.registrar_paciente import pantalla_registrar
from ui.cancelar_cita import ventana_cancelar
import ui.consultar_citas as cc
# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Sistema Hospital")
ventana.geometry("650x500")
ventana.configure(bg="#E3F2FD")

# -------------------------
# LIMPIAR PANTALLA
# -------------------------
def limpiar():
    for widget in contenedor.winfo_children():
        widget.destroy()

# -------------------------
# MENÚ PRINCIPAL
# -------------------------
def menu_principal():
    limpiar()

    tk.Label(contenedor, text="Sistema Hospital",
             font=("Arial", 20, "bold"),
             bg="#E3F2FD").pack(pady=30)

    tk.Button(contenedor, text="Recepcionista",
              bg="#1976D2", fg="white",
              width=25, height=2,
              relief="flat",
              command=menu_recepcionista).pack(pady=10)

    tk.Button(contenedor, text="Paciente",
              bg="#4CAF50", fg="white",
              width=25, height=2,
              relief="flat",
              command=menu_paciente).pack(pady=10)

# -------------------------
# RECEPCIONISTA
# -------------------------
def menu_recepcionista():
    limpiar()

    tk.Label(contenedor, text="Recepcionista",
             font=("Arial", 18, "bold"),
             bg="#E3F2FD").pack(pady=20)

    tk.Button(contenedor, text="Registrar Paciente",
              bg="#1976D2", fg="white",
              width=25, height=2,
              command=lambda: pantalla_registrar(contenedor, menu_recepcionista)
    ).pack(pady=10)

    tk.Button(contenedor, text="← Volver",
              command=menu_principal).pack(pady=20)

# -------------------------
# PACIENTE
# -------------------------
def menu_paciente():
    limpiar()

    tk.Label(contenedor, text="Paciente",
             font=("Arial", 18, "bold"),
             bg="#E3F2FD").pack(pady=20)

    tk.Button(contenedor, text="Agendar Cita",
              bg="#4CAF50", fg="white",
              width=25, height=2).pack(pady=5)

    tk.Button(contenedor, text="Consultar Citas",
              bg="#4CAF50", fg="white",
              width=25, height=2,
              command=lambda: cc.mostrar_citas(contenedor, menu_paciente)
    ).pack(pady=5)
    tk.Button(contenedor, text="Cancelar Cita",
              bg="#E53935", fg="white",
              width=25, height=2,
              command=lambda: ventana_cancelar(contenedor, menu_paciente)
    ).pack(pady=5)

    tk.Button(contenedor, text="← Volver",
              command=menu_principal).pack(pady=20)

# -------------------------
# CONTENEDOR
# -------------------------
contenedor = tk.Frame(ventana, bg="#E3F2FD")
contenedor.pack(fill="both", expand=True)

menu_principal()
ventana.mainloop()
# prueba