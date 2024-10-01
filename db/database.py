import sqlite3
from sqlite3 import Error

def conectar_db():
    try:
        conn = sqlite3.connect('db/usuarios.db')
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return None

def crear_tabla_usuarios():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL UNIQUE,
                                imagen_rostro TEXT,
                                huella TEXT)''')
            conn.commit()
            print("Tabla de usuarios creada correctamente")
        except Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            conn.close()

def registrar_usuario(nombre_usuario, imagen_rostro, huella):
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO usuarios (usuario, imagen_rostro, huella)
                              VALUES (?, ?, ?)''', (nombre_usuario, imagen_rostro, huella))
            conn.commit()
            print(f"Usuario {nombre_usuario} registrado correctamente")
        except Error as e:
            print(f"Error al registrar usuario: {e}")
        finally:
            conn.close()

def obtener_usuario(nombre_usuario):
    """
    Recupera la información de un usuario desde la base de datos utilizando su nombre de usuario.
    Devuelve el nombre de usuario y la ruta de la imagen de rostro.
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT usuario, imagen_rostro FROM usuarios WHERE usuario = ?", (nombre_usuario,))
            usuario = cursor.fetchone()  # Devuelve una tupla (usuario, imagen_rostro) si el usuario existe
            return usuario
        except Error as e:
            print(f"Error al obtener el usuario: {e}")
        finally:
            conn.close()
    return None
