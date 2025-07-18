# database.py
# Este módulo se encarga de la conexión y creación de las tablas en la base de datos SQLite.

import sqlite3
import random
import datetime

# Nombre del archivo de base de datos SQLite
DB_NAME = "inventario.db"

def connect():
    # Establece la conexión con la base de datos SQLite.
    # Retorna: Objeto de conexión a la base de datos.
    return sqlite3.connect(DB_NAME)

def cargarProductosIniciales():
    # Inserta 10 productos de ejemplo si la tabla está vacía.
    ruta_1 = 'https://www.shutterstock.com/image-photo/indonesia-mar-11-24-dell-600nw-2466605253.jpg'   # Laptop dell
    ruta_2 = 'https://i.ebayimg.com/images/g/OhAAAOSw~5RfY1XX/s-l640.jpg' # Smartphone Samsung
    ruta_3 = 'https://pcmundocomputer.com.co/wp-content/uploads/2023/12/1-120.jpg' #Tecclado Logitech
    ruta_4 = 'https://exitocol.vtexassets.com/arquivos/ids/26898370/Monitor-V22v-FHD-HP-V22v-3585350_b.jpg?v=638762974149500000' # Monitor HP
    ruta_5 = 'https://assets2.razerzone.com/images/pnx.assets/e429c76f51b34a0ce9c368be025e58b8/razer-naga-left-handed-edition-500x500.png' # Mouse razer
    ruta_6 = 'https://tecnonacho.com/wp-content/uploads/2024/11/IMAGENES-PRODUCTOS-47-IPAD-10-GENERACION-64GB.jpeg' # Tablet Apple
    ruta_7 = 'https://dbsolutionsystem.com.co/wp-content/uploads/2021/02/5ef2311ef2e2bcanon-17.jpg' # Impresora Canon
    ruta_8 = 'https://techstorecolombia.com/wp-content/uploads/2022/05/Audfonos-Diadema-Sony-Mdr-xb450-Extra-Bass-20200311095014.1581290015.jpg' # Auriculares Sony
    ruta_9 = 'https://www.mediatekis.com.co/media/catalog/product/cache/7c37608a0ced941863e2dadf4d54b13d/2/6/26532_1.jpg' # Cámara Nikon
    ruta_10 = 'https://i.ebayimg.com/thumbs/images/g/SjMAAeSwBsZnvnhN/s-l1200.jpg' # Disco duro seagate

    productos = [
        ("Laptop", "Dell", 1200.99, "2025-05-10", ruta_1),
        ("Smartphone", "Samsung", 899.99, "2025-05-11", ruta_2),
        ("Teclado", "Logitech", 49.99, "2025-05-12", ruta_3),
        ("Monitor", "HP", 199.99, "2025-05-13", ruta_4),
        ("Mouse", "Razer", 29.99, "2025-05-14", ruta_5),
        ("Tablet", "Apple", 499.99, "2025-05-15", ruta_6),
        ("Impresora", "Canon", 159.99, "2025-05-16", ruta_7),
        ("Auriculares", "Sony", 79.99, "2025-05-17", ruta_8),
        ("Cámara", "Nikon", 599.99, "2025-05-18", ruta_9),
        ("Disco Duro", "Seagate", 89.99, "2025-05-19", ruta_10)
    ]
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany("INSERT INTO productos (nombre, marca, precio, ingreso, ruta_img) VALUES (?, ?, ?, ?, ?)", productos)
        conn.commit()
    conn.close()

def cargarListaEmpleados():
    """ Listas de datos para generar información aleatoria """
    nombres = ["Ana", "Juan", "Maria", "Carlos", "Laura", "Pedro", "Sofía", "Miguel", "Isabella", "Diego", "Valeria", "Javier", "Camila", "Andres", "Gabriela"]
    apellidos = ["García", "Rodríguez", "Martínez", "Hernández", "López", "González", "Pérez", "Sánchez", "Ramírez", "Flores", "Díaz", "Torres", "Ruiz", "Gómez", "Jiménez"]
    cargos = ["vendedor", "administrador", "ingeniero", "asistente", "gerente", "analista", "diseñador"]

    empleados = []

    for i in range(1, 40): # Generamos 15 empleados
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        # Generamos un número de identificación de 10 dígitos aleatorio
        identificacion = str(random.randint(1000000000, 1999999999))
        cargo = random.choice(cargos)
        # Generamos un número de teléfono de 10 dígitos aleatorio (simulando Colombia)
        telefono = "3" + str(random.randint(100000000, 249999999))
        email = f"{nombre.lower()}{apellido.lower()}{random.randint(1,100)}@example.com"
        # Fecha de contratación aleatoria en los últimos 5 años
        fecha_contratacion = (datetime.date.today() - datetime.timedelta(days=random.randint(0, 5*365))).strftime("%Y-%m-%d")

        empleado_info = (nombre, apellido, identificacion, cargo, telefono, email, fecha_contratacion)
        empleados.append(empleado_info)

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM empleados")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany("INSERT INTO empleados (nombre, apellido, DNI, cargo, telefono, email, ingreso) VALUES (?, ?, ?, ?, ?, ?, ?)", empleados)
        conn.commit()
    conn.close()

def initialize_db():
    """ Inicializa la base de datos y crea las tablas necesarias si no existen."""
    conn = connect()
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            cargo TEXT DEFAULT 'admin'
        )
    ''')

    # Crear tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT,
            precio REAL DEFAULT 0.0,
            ingreso TEXT,
            ruta_img TEXT NULL
        )
    ''')

    # Crear tabla de empleados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            DNI INTEGER NOT NULL,
            cargo TEXT NOT NULL,
            telefono INTEGER,
            email TEXT,
            ingreso TEXT
        )
    ''')

    # Confirmar cambios
    conn.commit()
    conn.close()

    # Cargar productos iniciales
    cargarProductosIniciales()
    cargarListaEmpleados()