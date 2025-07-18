import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from gestor_inventario.database import connect
import requests
from io import BytesIO

class InventoryManager(tk.Toplevel):
    def __init__(self, parent):
        # Definir variables implícitas
        super().__init__(parent)
        self.title("Gestión de Inventario")
        self.image_cache = {}  # Cache de imágenes

        # Establecer el tamaño de la ventana
        width = 900
        height = 500
        
        # Obtener el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular coordenadas para centrar la ventana
        x = (screen_width - width) // 2
        y = (screen_height - height) // 4

        # Establecer el tamaño y posición de la ventana
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.nombre_var = tk.StringVar()
        self.marca_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.ruta_img_var = tk.StringVar()
        self.fechaIngreso_var = tk.StringVar()

        self.crearWidgets()

        # Hacer modal la ventana
        self.transient(parent)
        self.grab_set()
        
    def crearWidgets(self):
        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        tk.Label(main_frame, text='INVENTARIO', font=("Arial", 18, "bold")).pack(pady=10)

        # Frame izquierdo: Formulario para ingreso de productos
        left_frame = tk.LabelFrame(main_frame, text="Agregar Producto")
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        campos = [("Nombre", self.nombre_var), ("Marca", self.marca_var), ("Precio", self.precio_var), ("URL de la imagen", self.ruta_img_var), ("Fecha", self.fechaIngreso_var)]
        
        # Bucle para crear los campos de ingreso de datos
        for label, var in campos:
            tk.Label(left_frame, text=label).pack(anchor="w", padx=10)
            tk.Entry(left_frame, textvariable=var, width=25).pack(fill="x", padx=10, pady=5)
        tk.Button(left_frame, text="Agregar", command=self.agregar_producto).pack(pady=5)

        # Frame central: lista de productos
        center_frame = tk.LabelFrame(main_frame, text="Lista de Productos")
        center_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        tree_frame = tk.Frame(center_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columnas = ["ID", "Nombre", "Marca", "Precio", "Fecha"]
        widths = [50, 100, 100, 60, 100]
        self.tree = ttk.Treeview(tree_frame, columns=columnas, show="headings")
        
        # Bucle para configurar columnas y encabezados
        for col, width in zip(columnas, widths):
            self.tree.column(col, width=width)
            self.tree.heading(col, text=col)

        # Habilitar edición en doble clic
        self.tree.bind("<Double-1>", self.editar_celda)
        self.tree.bind("<<TreeviewSelect>>", self.cargar_imagen)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Botones para editar y eliminar
        button_frame = tk.Frame(center_frame)
        button_frame.pack(pady=10)
        bottons = [('Eliminar', self.eliminar_producto), ('Actualizar', self.editar_producto)]
        for name, function in bottons:
            tk.Button(button_frame, text=name, command=function).pack(side='right',padx=5)

        # Frame derecho: Visualización del producto
        right_frame = tk.LabelFrame(main_frame, text="Visualización de Producto")
        right_frame.pack(side="left", fill="y", padx=5, pady=5)
        self.imagen_label = tk.Label(right_frame, text="Sin imagen", bg="gray", width=25, height=13)
        self.imagen_label.pack(padx=10, pady=10)
        #tk.Button(right_frame, text="Cargar Imagen", command=self.cargar_imagen).pack(pady=5)

        # Carga los prodcutos de la DB
        self.cargar_productos()

    def agregar_producto(self):
        """ Método para agragr productos a la tabla productos"""
        nombre = self.nombre_var.get()
        marca = self.marca_var.get()
        precio = self.precio_var.get()
        ruta_img = self.ruta_img_var.get()
        ingreso = self.fechaIngreso_var.get()

        if not nombre or not marca or not precio or not ingreso:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        
        else:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombre, marca, precio, ingreso, ruta_img) VALUES (?, ?, ?, ?, ?)",
                        (nombre, marca, precio, ingreso, ruta_img))
            conn.commit()
            conn.close()
            self.cargar_productos()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")

    def cargar_productos(self):
        """ Cargar los productos desde la base de datos"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conn.close()

        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar productos en el Treeview
        for producto in productos:
            self.tree.insert("", "end", values=producto)

    def cargar_imagen(self, event):
        # Obtener el registro seleccionado
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        # Verificar si hay un registro seleccionado y si la lista no está vacía
        if not selected or not values:
            return

        product_id = int(values[0])

        # Verificar si la imagen ya está en la caché
        if product_id in self.image_cache:
            img = self.image_cache[product_id]
            self.imagen_label.config(image=img, width=150, height=100)
            #self.imagen_label.image = img
            return
        
        # Obtener la URL de la imagen desde la base de datos
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ruta_img FROM productos WHERE id=?", (product_id,))
        url_img = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        # Verificar si el resultado es None o la URL está vacía
        if not url_img:
            # Mostrar mensaje "Imagen no encontrada" en el label
            self.imagen_label.config(text="Imagen no encontrada", image="", width=20, height=10)
            return

        try:
            response = requests.get(url_img, timeout=5)
            if response.status_code == 200:
                # Descargar y cargar la imagen si no está en la caché
                img = Image.open(BytesIO(response.content)).resize((150, 150))
                img = ImageTk.PhotoImage(img)

                # Guardar en la caché para futuros usos
                self.image_cache[product_id] = img

                # Mostrar la imagen
                self.imagen_label.config(image=img, width=150, height=100)
                #self.imagen_label.image = img

            else:
                self.imagen_label.config(text="Imagen no encontrada", image="", width=20, height=10)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def editar_celda(self, event):
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
        entry.bind("<Return>", lambda e: self.actualizar_celda(item, column_index, entry.get()))
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def actualizar_celda(self, item, column_index, value):
        values = list(self.tree.item(item, 'values'))
        values[column_index] = value
        self.tree.item(item, values=values)            

    def editar_producto(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un producto para guardar cambios")
                return
            
            values = self.tree.item(selected, "values")
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET nombre=?, marca=?, precio=?, ingreso=? WHERE id= ?", (values[1], values[2], values[3], values[4], values[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al editar el producto: {e}")

    def eliminar_producto(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")

            else:
                values = self.tree.item(selected, "values")
                product_id = values[0]

                conn = connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE id=?", (product_id,))
                conn.commit()
                conn.close()

                self.cargar_productos()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el producto: {e}")

# Porción de código que permite ejecutar de manera independiente
    def run(self):
        self.cargar_productos()
        self.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManager(root)
    app.run()