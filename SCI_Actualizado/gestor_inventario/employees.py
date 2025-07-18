# employees.py

import tkinter as tk
from tkinter import ttk, messagebox
from gestor_inventario.database import connect

class EmployeesManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Empleados")
        self.geometry("850x550")

        # Establecer tamaño de la ventana
        width = 1000
        height = 550

        # Obtener el tamaño de la ventan
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Coordenadas para centrar la ventana
        x = (screen_width - width) // 2
        y = (screen_height - height) // 4

        # Establecer el tamaño y la posición
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.dni_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.cargo_var = tk.StringVar()
        self.fechaingreso_var = tk.StringVar()

        self.crearWidgets()

        # Hacer modal la ventana
        self.transient(parent)
        self.grab_set()

    def crearWidgets(self):
        """ Crea los widgets visuales de la ventana"""
        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(side="left", fill="y", padx=5, pady=5)
        tk.Label(main_frame, text="EMPLEADOS", font=("Arial", 18, "bold")).pack(pady=10)

        # Frame izquierdo: Formulario para ingreso de personal
        left_frame = tk.LabelFrame(main_frame, text="Agregar Empleado")
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        campos = [("Nombre", self.nombre_var), ("Apellido", self.apellido_var), ("DNI", self.dni_var), ("Cargo", self.cargo_var), ("Teléfono", self.telefono_var), ("Email", self.email_var), ("Fecha", self.fechaingreso_var)]

        # Bucle para crear campos de ingreso
        for label, var in campos:
            tk.Label(left_frame, text=label).pack(anchor="w", padx=10)
            tk.Entry(left_frame, textvariable=var, width=30).pack(fill="x", padx=10, pady=5)
        tk.Button(left_frame, text="Agregar", command=self.agregarEmpleado).pack(pady=5)

        # Frame central: Treeview para listar empleados
        right_frame = tk.LabelFrame(main_frame, text="Lista de Empleados")
        right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        tree_frame = tk.Frame(right_frame)
        tree_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        columnas = ["ID", "Nombre", "Apellido", "DNI", "Cargo", "Telefono", "Email", "Fecha Ingreso"]
        widths = [50, 100, 100, 50, 100, 100, 200, 100]
        self.tree = ttk.Treeview(tree_frame, columns=columnas, show="headings")

        # Bucle para configurar columnas y encabezados
        for col, width in zip(columnas, widths):
            self.tree.column(col, width=width)
            self.tree.heading(col, text=col)

        # Habilitar edición en doble clic
        self.tree.bind("<Double-1>", self.editarCelda)

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Botones para editar y eliminar
        buttons_frame = tk.Frame(right_frame)
        buttons_frame.pack(side="bottom", pady=10)
        buttons = [("Eliminar", self.eliminarEmpleado), ("Actualizar", self.editarEmpleado)]
        for name, function in buttons:
            tk.Button(buttons_frame, text=name, command=function).pack(side="right", padx=5)

        # Cargar los empleados de la DB
        self.cargarEmpleados()

    def agregarEmpleado(self):
        nombre = self.nombre_var.get()
        apellido = self.apellido_var.get()
        id = self.dni_var.get()
        cargo = self.cargo_var.get()
        telefono = self.telefono_var.get()
        email = self.email_var.get()
        ingreso = self.fechaingreso_var.get()

        if not nombre or not apellido or not id or not cargo or not telefono or not email or not ingreso:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        
        else:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO empleados (nombre, apellido, DNI, cargo, telefono, email, ingreso) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (nombre, apellido, id, cargo, telefono, email, ingreso))
            conn.commit()
            conn.close()
            self.cargarEmpleados()
            messagebox.showinfo("Éxito", "Empleado agregado correctamente")

    def cargarEmpleados(self):
        # Cargar los empelados desde la base de datos
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
        conn.close()

        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Cargar la lista de empleados en el Treeview
        for empleado in empleados:
            self.tree.insert("", "end", values=empleado)

    def editarCelda(self, event):
        # Hacer la celda editable al hacer doble clic
        item = self.tree.focus()
        if not item:
            return
        
        column = self.tree.identify_column(event.x)[1:]
        column_index = int(column) - 1

        # Verificar si la columna es la primera (id) para evitar edición
        if column_index == 0:
            return

        x, y, width, height = self.tree.bbox(item, column)
        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, self.tree.item(item, 'values')[column_index])
        entry.focus()
        entry.bind("<Return>", lambda e: self.actualizarCelda(item, column_index, entry.get()))
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def actualizarCelda(self, item, column_index, value):
        values = list(self.tree.item(item, 'values'))
        values[column_index] = value
        self.tree.item(item, values=values)

    def editarEmpleado(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un empleado para efectuar cambios")
                return
            
            values = self.tree.item(selected, "values")
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE empleados SET nombre=?, apellido=?, DNI=?, cargo=?, telefono=?, email=?, ingreso=? WHERE id= ?", (values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el empleado: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al editar el empleado: {e}")
  
    def eliminarEmpleado(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")

            else:
                values = self.tree.item(selected, "values")
                product_id = values[0]

                conn = connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM empleados WHERE id=?", (product_id,))
                conn.commit()
                conn.close()

                self.cargarEmpleados()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el empleado: {e}")


# Porción de código que permite ejecutar de manera independiente
    def run(self):
        self.cargarEmpleados()
        self.mainloop()

if __name__ == "__main__":
    #root = tk.Tk()
    app = EmployeesManager(tk.Tk())
    app.run()