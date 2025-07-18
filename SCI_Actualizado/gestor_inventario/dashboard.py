import tkinter as tk
from gestor_inventario.inventory import InventoryManager
from gestor_inventario.employees import EmployeesManager
from gestor_inventario.users import UsersManager

class Dashboard(tk.Frame):
    """
    Panel de control principal de la aplicación.
    Contiene botones para acceder a las diferentes funcionalidades.
    """
    def __init__(self, parent, on_logout_callback):
        super().__init__(parent)
        self.parent = parent
        self.on_logout_callback = on_logout_callback
        # self.pack(fill="both", expand=True) # El dashboard ocupará toda la ventana principal

        self._create_widgets()

    def _create_widgets(self):
        """Crea los botones para las diferentes funcionalidades."""
        tk.Label(self, text="Panel de Control Principal", font=("Arial", 16, "bold")).pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Gestión de Inventario", command=self._open_gestion_inventario, width=25, height=2).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Lista de Empleados", command=self._open_lista_empleados, width=25, height=2).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Lista de Usuarios", command=self._open_lista_usuarios, width=25, height=2).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Gestión de Proveedores", command=self._open_gestion_proveedores, width=25, height=2).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Reportes", command=self._open_reportes, width=25, height=2).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Sistema de Ventas", command=self._open_sistema_ventas, width=25, height=2).grid(row=2, column=1, padx=10, pady=10)
       
        # Botón para cerrar sesión
        tk.Button(self, text="Cerrar Sesión", command=self.on_logout_callback, bg="red", fg="white", font=("Arial", 10, "bold")).pack(pady=20)
       
    # Las funciones _open_xxx permanecen sin cambios
    def _open_gestion_inventario(self):
        InventoryManager(self.parent)

    def _open_lista_empleados(self):
        EmployeesManager(self.parent)

    def _open_lista_usuarios(self):
        UsersManager(self.parent)

    def _open_gestion_proveedores(self):
        GestionProveedoresWindow(self.parent)

    def _open_reportes(self):
        ReportesWindow(self.parent)

    def _open_sistema_ventas(self):
        SistemaVentasWindow(self.parent)

# --- Módulos de Funcionalidad (Ejemplos con prints) ---
class GestionProveedoresWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Proveedores")
        self.geometry("600x400")
        tk.Label(self, text="Aquí iría la funcionalidad de Gestión de Proveedores").pack(pady=20)
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)
        self.transient(parent)
        self.grab_set()

class ReportesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reportes")
        self.geometry("700x500")
        tk.Label(self, text="Aquí iría la funcionalidad de Reportes").pack(pady=20)
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)
        self.transient(parent)
        self.grab_set()

class SistemaVentasWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sistema de Ventas")
        self.geometry("800x600")
        tk.Label(self, text="Aquí iría la funcionalidad del Sistema de Ventas").pack(pady=20)
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)
        self.transient(parent)
        self.grab_set()