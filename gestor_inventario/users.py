import tkinter as tk
from tkinter import ttk, messagebox
from gestor_inventario.database import connect

class UsersManager (tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de usuarios")
        
        # Establecer el tamaño de la ventana
        width, height = 750, 450
        
        # Calcular coordenadas para centrar la ventanas
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 4

        # Establecer el tamaño y posición de la ventana
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.nombre_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.cargo_var = tk.StringVar()
        
        self.crearWidgets()

        # Hacer modular
        self.transient(parent)
        self.grab_set()

    def crearWidgets(self):
        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(side="left", fill="y", padx=5, pady=5)
        tk.Label(main_frame, text="ADMINISTRADOR DE USUARIOS", font=("Arial", 18, "bold")).pack(pady=10)

        # Frame izquierdo: Formulario para ingreso de usuarios
        left_frame = tk.LabelFrame(main_frame, text="Agregar Usuario")
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        campos = [("Nombre", self.nombre_var), ("Email", self.email_var), ("Password", self.password_var), ("Role", self.cargo_var)]

        # Bucle para crear campos de ingreso
        for label, var in campos:
            tk.Label(left_frame, text=label).pack(anchor="w", padx=10)
            tk.Entry(left_frame, textvariable=var, width=30).pack(fill="x", padx=10, pady=5)
        tk.Button(left_frame, text="Agregar", command=self.agregarUsuario).pack(pady=5)

        # Frame central: Treeview para listar empleados
        right_frame = tk.LabelFrame(main_frame, text="Lista de Empleados")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        tree_frame = tk.Frame(right_frame)
        tree_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        columnas = ["ID", "Nombre", "Email", "Password", "Role"]
        widths = [50, 120, 120, 80, 90]
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
        buttons_frame.pack(side="bottom", padx=10, pady=10)
        buttons = [("Eliminar", self.eliminarUsuario), ("Actualizar", self.editarUsuario)]
        for name, function in buttons:
            tk.Button(buttons_frame, text=name, command=function).pack(side="right", padx=5)

        # Cargar los usuario de la DB
        self.cargarUsuarios()

    def editarCelda(self, event):
        # Hacer la celda editable al hacer doble clic
        item = self.tree.focus()
        if not item:
            return
        
        column = self.tree.identify_column(event.x)[1:]
        column_index = int(column)-1

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

    def cargarUsuarios(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Cargar empleados en treeview
        for usuario in usuarios:
            self.tree.insert("", "end", values=usuario)

    def agregarUsuario (self):
        nombre = self.nombre_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        cargo = self.cargo_var.get()

        if not nombre or not email or not password or not cargo:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

        else:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email, password, cargo) VALUES (?, ?, ?, ?)",
                           (nombre, email, password, cargo))
            conn.commit()
            conn.close()
            self.cargarUsuarios()
            messagebox.showinfo("Éxito", "Empleado agregado correctamente")

    def eliminarUsuario(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")

            else:
                values = self.tree.item(selected, "values")
                user_id = values[0]

                conn = connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
                conn.commit()
                conn.close()

                self.cargarUsuarios()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el empleado: {e}")


    def editarUsuario(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un empleado para efectuar cambios")
                return
            
            values = self.tree.item(selected, "values")
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET nombre=?, email=?, password=?, cargo=? WHERE id= ?", (values[1], values[2], values[3], values[4], values[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el empleado: {e}")

    # Porción de código que permite ejecutar de manera independiente
    def run(self):
        self.cargarUsuarios()
        self.mainloop()

if __name__ == "__main__":
    #root = tk.Tk()
    app = UsersManager(tk.Tk())
    app.run()