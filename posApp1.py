# --- Clase Principal de la Aplicación (Ahora gestiona el cambio de Frame) ---
import tkinter as tk
from gestor_inventario.dashboard import Dashboard
from gestor_inventario.login import LoginFrame
from gestor_inventario.database import initialize_db
from PIL import Image, ImageTk

class POSApp(tk.Tk):
    """
    Clase principal de la aplicación POS.
    Gestiona la inicialización de la ventana y el flujo entre Login y Dashboard
    como frames DENTRO de la misma ventana principal.
    """
    def __init__(self):
        super().__init__()
        self.title("Sistema POS - Tienda")
        self.geometry("800x600")
        self.resizable(False, False) # Evitar que la ventana principal cambie de tamaño
        
        # Cargar el canvas con la imagen
        self._cargar_fondo()
       
        # Centrar la ventana principal en la pantalla
        self.update_idletasks() # Procesar todos los eventos pendientes antes de actualizar widgets
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 4
        self.geometry(f'+{x}+{y}')
        
        # Crear instancias de los frames (Login y Dashboard)
        # Siguen siendo hijos de la ventana principal (self)
        self.login_frame = LoginFrame(self, self._show_dashboard_view)
        self.dashboard_frame = Dashboard(self, self._show_login_view) # Callback para cerrar sesión

        # Inicializar vistas con place_forget ---
        # Aseguramos que ambos frames no estén "placeados" al inicio
        self.login_frame.place_forget()
        self.dashboard_frame.place_forget()

        self._show_login_view() # Mostrar la vista de login al inicio

    def _cargar_fondo(self):
        # Cargar la imagen
        try:
            self.image = Image.open(r"C:/Users/Windows/Desktop/SCI actualizado/Images/almacen2.jpg")  # Reemplaza con el nombre de tu archivo
            resized_image = self.image.resize((800, 600), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print("Error: Archivo de imagen no encontrado.")
            return
        
        # Crear un Canvas
        self.canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        self.canvas.pack(fill="both", expand=True)

        # Dibujar la imagen en el Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

    def _clear_view(self):
        """Oculta todos los frames actualmente visibles."""
        for widget in self.winfo_children():
            # Solo queremos olvidar los frames de vista (LoginApp, Dashboard)
            # no los Toplevels de módulos de funcionalidad
            if isinstance(widget, (LoginFrame, Dashboard, tk.Frame, tk.LabelFrame)):
                widget.place_forget()

    def _show_login_view(self):
        """Muestra el frame de login."""
        self._clear_view()
        # Posicionar LoginFrame con place ---
        # place coloca el widget en coordenadas relativas a su padre (la ventana principal en este caso)
        # relx, rely, relwidth, relheight: 0.5 = 50%, 1.0 = 100%
        # anchor="center": el centro del widget se alinea con las coordenadas dadas (0.5, 0.5 = centro de la ventana)
        self.login_frame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.55, anchor="center")
        self.login_frame.lift() # Asegura que el login_frame esté en primer plano
        self.login_frame.email.focus_set() # Poner el foco en el campo de usuario

    def _show_dashboard_view(self):
        """Muestra el frame del dashboard."""
        self._clear_view()
        # Posicionar Dashboard con place ---
        self.dashboard_frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.6, anchor="center")
        self.dashboard_frame.lift() # Asegura que el dashboard_frame esté en primer plano

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        initialize_db()
        self.mainloop()

if __name__ == "__main__":
    app = POSApp()
    app.run()