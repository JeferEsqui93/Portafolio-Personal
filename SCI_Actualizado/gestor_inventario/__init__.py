"""
Paquete gestor_inventario
Este módulo contiene la lógica principal del sistema de control de inventario:
- Conexión y manejo de la base de datos
- Interfaz gráfica del inventario
"""

"""

# Importaciones clave para facilitar el acceso desde fuera del paquete
from .database import connect  # Permite importar directamente con: from gestor_inventario import connect
from .inventory import InventoryManager  # Clase principal de la GUI de inventario

# Información del paquete (opcional pero útil)
__version__ = "1.0.0"
__author__ = "Jefferson Esquivel"
"""