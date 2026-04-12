import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar

def ventana_cancelar(contenedor, volver):

    def pantalla_buscar():
        for widget in contenedor.winfo_children():
            widget.destroy()

        tk.Label(contenedor, text="Cancelar Cita",
                 font=("Arial", 18, "bold"),
                 bg="#E3F2FD").pack(pady=20)

        tk.Label(contenedor, text="Ingresa tu número de CI:",
                 bg="#E3F2FD", font=("Arial", 12)).pack(pady=5)

        entry_ci = tk.Entry(contenedor, font=("Arial", 13), width=25)
        entry_ci.pack(pady=5)

        def buscar_citas():
            ci = entry_ci.get().strip()
            if not ci:
                messagebox.showwarning("Aviso", "Ingresa tu CI")
                return
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM pacientes WHERE ci = %s", (ci,))
                paciente = cursor.fetchone()
                if not paciente:
                    messagebox.showerror("Error", "No se encontró paciente con ese CI")
                    conn.close()
                    return
                paciente_id = paciente[0]
                cursor.execute("""
                    SELECT c.id, c.medico, c.fecha, c.hora, c.estado
                    FROM citas c
                    WHERE c.paciente_id = %s
                    ORDER BY c.fecha ASC
                """, (paciente_id,))
                citas = cursor.fetchall()
                conn.close()
                pantalla_citas(citas, paciente_id)
            except Exception as e:
                messagebox.showerror("Error de conexión", str(e))

        tk.Button(contenedor, text="Buscar mis citas",
                  bg="#1976D2", fg="white",
                  width=20, height=2,
                  command=buscar_citas).pack(pady=10)

        tk.Button(contenedor, text="← Volver",
                  command=volver).pack(pady=5)

    def pantalla_citas(citas, paciente_id):
        for widget in contenedor.winfo_children():
            widget.destroy()

        tk.Label(contenedor, text="Mis Citas",
                 font=("Arial", 18, "bold"),
                 bg="#E3F2FD").pack(pady=15)

        if not citas:
            tk.Label(contenedor, text="No tienes citas registradas.",
                     bg="#E3F2FD", font=("Arial", 12)).pack(pady=20)
        else:
            columnas = ("ID", "Médico", "Fecha", "Hora", "Estado")
            tabla = ttk.Treeview(contenedor, columns=columnas,
                                 show="headings", height=6)
            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=95)

            # Colores según estado
            tabla.tag_configure("activa",    background="#C8E6C9")  # verde
            tabla.tag_configure("cancelada", background="#FFCDD2")  # rojo

            for fila in citas:
                tag = "activa" if fila[4] == "Activa" else "cancelada"
                tabla.insert("", "end", values=fila, tags=(tag,))

            tabla.pack(padx=10, pady=5)

            def cancelar_seleccion():
                seleccion = tabla.selection()
                if not seleccion:
                    messagebox.showwarning("Aviso", "Selecciona una cita")
                    return
                fila = tabla.item(seleccion[0])["values"]
                # Verificar si ya está cancelada
                if fila[4] == "Cancelada":
                    messagebox.showwarning(
                        "Aviso",
                        "Esta cita ya fue cancelada, no puedes cancelarla de nuevo."
                    )
                    return
                id_cita = fila[0]
                confirmar = messagebox.askyesno(
                    "Confirmar",
                    f"¿Cancelar cita con {fila[1]} el {fila[2]}?"
                )
                if confirmar:
                    try:
                        conn = conectar()
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE citas SET estado = 'Cancelada' WHERE id = %s",
                            (id_cita,)
                        )
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Éxito", "¡Cita cancelada! ✅")
                        # Recargar citas
                        conn2 = conectar()
                        cursor2 = conn2.cursor()
                        cursor2.execute("""
                            SELECT c.id, c.medico, c.fecha, c.hora, c.estado
                            FROM citas c
                            WHERE c.paciente_id = %s
                            ORDER BY c.fecha ASC
                        """, (paciente_id,))
                        citas_nuevas = cursor2.fetchall()
                        conn2.close()
                        pantalla_citas(citas_nuevas, paciente_id)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            tk.Button(contenedor, text="❌ Cancelar Cita Seleccionada",
                      bg="#E53935", fg="white",
                      width=25, height=2,
                      command=cancelar_seleccion).pack(pady=10)

        def salir():
            confirmar = messagebox.askyesno("Salir", "¿Seguro que quieres salir?")
            if confirmar:
                volver()

        tk.Button(contenedor, text="🚪 Salir",
                  bg="#757575", fg="white",
                  width=25, height=2,
                  command=salir).pack(pady=10)

    pantalla_buscar()