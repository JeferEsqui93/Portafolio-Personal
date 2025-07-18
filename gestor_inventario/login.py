# login.py
# Gestión de login y registro en una sola ventana utilizando el método crearWidgets() para crear los elementos gráficos.

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from gestor_inventario.database import connect

class LoginFrame(tk.Frame):
    def __init__(self, parent, on_login_success_callback):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success_callback = on_login_success_callback
       
        self.mode = "login"
        self.upper_label = "INICIO DE SESIÓN"
        self.create_widgets()


    # Función que crea los elementos visuales (labels, bottons, entre otros)
    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        # Crear un main_frame para contener los widgets
        ttk.Label(self, text=self.upper_label, font=("Arial", 18, "bold")).pack(pady=10)

        ttk.Label(self, text='Email').pack(padx=5, pady=2)
        self.email = ttk.Entry(self, width=30)
        self.email.pack(padx=5, pady=2)

        ttk.Label(self, text='Contraseña').pack(padx=5, pady=2)
        self.password = ttk.Entry(self, width=30, show="*")
        self.password.pack(padx=5, pady=2)
        
        if self.mode == "register":
            ttk.Label(self, text="Nombre:").pack(padx=5, pady=2)
            self.nombre = ttk.Entry(self, width=30)
            self.nombre.pack(padx=5, pady=2)

        action = self.register_user if self.mode == "register" else self.login_user
        ttk.Button(self, text="Registrarse" if self.mode == "register" else "Iniciar sesión", command=action).pack(pady=5)

        # Botón para realizar el registro
        ttk.Button(
            self,
            text="¿Nuevo usuario? Regístrate aquí" if self.mode == "login" else "¿Ya tienes cuenta? Inicia sesión",
            command=self.toggle_mode
        ).pack(pady=5)

        # Botón para salir de la app
        ttk.Button(self, text="Salir", command=self.quit).pack(pady=5)

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.upper_label = "REGISTRO DE USUARIO"
        else:
            self.mode = "login"
            self.upper_label= "INICIO DE SESIÓN"
        
        self.create_widgets()

    def register_user(self):
        nombre = self.nombre.get()
        email = self.email.get()
        password = self.password.get()

        if not nombre or not email or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        conn = connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", (nombre, email, password))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado. Ahora puedes iniciar sesión.")
            self.toggle_mode()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El correo ya está registrado.")
        finally:
            conn.close()

    def login_user(self):
        email = self.email.get()
        password = self.password.get()

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM usuarios WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.on_login_success_callback()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")