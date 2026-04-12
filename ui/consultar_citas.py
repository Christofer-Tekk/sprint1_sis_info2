from conexion import conectar
import tkinter as tk

def mostrar_citas(contenedor, volver):
    # limpiar pantalla
    for widget in contenedor.winfo_children():
        widget.destroy()

    tk.Label(contenedor, text="Consultar Citas",
             font=("Arial", 18, "bold"),
             bg="#E3F2FD").pack(pady=20)

    tk.Label(contenedor, text="Ingrese CI:",
             bg="#E3F2FD").pack()

    entry_ci = tk.Entry(contenedor)
    entry_ci.pack(pady=5)

    resultado_label = tk.Label(contenedor, text="", bg="#E3F2FD", justify="left")
    resultado_label.pack(pady=10)

    def buscar():
        ci = entry_ci.get().strip()

        if ci == "":
            resultado_label.config(text="⚠️ Ingrese CI")
            return

        # 🔥 AQUÍ TE CONECTAS A LA BD
        conn = conectar()
        cursor = conn.cursor()

        # 🔎 BUSCAR PACIENTE
        cursor.execute("SELECT id FROM pacientes WHERE ci = %s", (ci,))
        paciente = cursor.fetchone()

        if not paciente:
            resultado_label.config(text="❌ Paciente no encontrado")
            cursor.close()
            conn.close()
            return

        paciente_id = paciente[0]

        # 🔎 BUSCAR CITAS DEL PACIENTE
        cursor.execute("""
            SELECT medico, fecha, hora, estado
            FROM citas
            WHERE paciente_id = %s
            ORDER BY fecha ASC
        """, (paciente_id,))

        citas = cursor.fetchall()

        cursor.close()
        conn.close()

        # 🔴 VALIDACIONES
        if not citas:
            resultado_label.config(text="📭 No tiene citas programadas")
            return

        # ✅ MOSTRAR RESULTADO
        texto = "📅 Citas:\n\n"
        for i, c in enumerate(citas, start=1):
            texto += f"Cita {i}\n"
            texto += f" Médico: {c[0]}\n"
            texto += f" Fecha: {c[1]}\n"
            texto += f" Hora: {c[2]}\n"
            texto += f" Estado: {c[3]}\n"
            texto += "------------------\n"

        resultado_label.config(text=texto)

    tk.Button(contenedor, text="Buscar",
              bg="#1976D2", fg="white",
              command=buscar).pack(pady=10)

    tk.Button(contenedor, text="← Volver",
              command=volver).pack(pady=20)