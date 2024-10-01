import tkinter as tk
import cv2
import os
from tkinter import messagebox
from db.database import crear_tabla_usuarios, registrar_usuario, obtener_usuario
from biometria.captura_rostro import capturar_rostro
from biometria.captura_huella import capturar_huella
from biometria.face_comparation import compare_faces

def iniciar_sesion_admin():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    
    if usuario == "admin" and contrasena == "admin123":
        messagebox.showinfo("Login exitoso", "Bienvenido, administrador")
        abrir_vista_admin()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

def abrir_vista_admin():
    admin_window = tk.Toplevel(root)
    admin_window.title("Vista Administrador")

    label = tk.Label(admin_window, text="Registro de Usuarios")
    label.pack()

    label_usuario = tk.Label(admin_window, text="Nombre de Usuario:")
    label_usuario.pack()
    entry_nombre_usuario = tk.Entry(admin_window)
    entry_nombre_usuario.pack()

    # Variables para almacenar los nombres de los archivos de rostro y huella
    nombre_archivo_rostro = None
    nombre_archivo_huella = None

    # Función para capturar el rostro
    def capturar_rostro_usuario():
        nonlocal nombre_archivo_rostro
        nombre_usuario = entry_nombre_usuario.get()
        nombre_archivo_rostro = capturar_rostro(nombre_usuario)
        messagebox.showinfo("Captura de Rostro", "Rostro capturado exitosamente")

    # Función para capturar la huella
    def capturar_huella_usuario():
        nonlocal nombre_archivo_huella
        nombre_usuario = entry_nombre_usuario.get()
        nombre_archivo_huella = capturar_huella(nombre_usuario)
        messagebox.showinfo("Captura de Huella", "Huella capturada exitosamente")

    # Botón para capturar la foto del rostro
    btn_capturar_rostro = tk.Button(admin_window, text="Capturar Rostro", 
                                    command=capturar_rostro_usuario)
    btn_capturar_rostro.pack()

    # Botón para capturar la huella dactilar
    btn_capturar_huella = tk.Button(admin_window, text="Capturar Huella", 
                                    command=capturar_huella_usuario)
    btn_capturar_huella.pack()

    # Función para registrar al usuario después de capturar rostro y huella
    def registrar_usuario_completo():
        nombre_usuario = entry_nombre_usuario.get()
        if nombre_archivo_rostro and nombre_archivo_huella:
            registrar_usuario(nombre_usuario, nombre_archivo_rostro, nombre_archivo_huella)
            messagebox.showinfo("Registro exitoso", f"Usuario {nombre_usuario} registrado correctamente")
        else:
            messagebox.showerror("Error", "Debes capturar el rostro y la huella antes de registrar")

    # Botón para registrar el usuario (se debe haber capturado el rostro y la huella antes)
    btn_registrar = tk.Button(admin_window, text="Registrar Usuario", command=registrar_usuario_completo)
    btn_registrar.pack()

def capturar_rostro_verificacion(nombre_usuario):
    """
    Captura una imagen de rostro desde la cámara y la guarda con un nombre basado en el usuario para la verificación.
    Devuelve la ruta de la imagen capturada.
    """
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Captura de Rostro para Verificación")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error al acceder a la cámara")
            break

        cv2.imshow("Captura de Rostro para Verificación", frame)

        # Presionar 'q' para capturar la imagen y salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Crear el nombre del archivo basándonos en el usuario y la fecha/hora
            ruta_imagen_capturada = f'static/captures/faces/{nombre_usuario}_verificacion.png'
            cv2.imwrite(ruta_imagen_capturada, frame)
            print(f"Imagen capturada y guardada en {ruta_imagen_capturada}")
            break

    cam.release()
    cv2.destroyAllWindows()

    return ruta_imagen_capturada


def validar_identidad():
    nombre_usuario = entry_usuario.get()

    # Obtener el usuario y su imagen de rostro almacenada
    usuario = obtener_usuario(nombre_usuario)

    if usuario:
        messagebox.showinfo("Usuario encontrado", "Capturando imagen para validación")

        # Capturar la imagen del rostro para la verificación
        imagen_capturada_url = capturar_rostro_verificacion(nombre_usuario)

        try:
            usuarioBD = usuario[1]
            # Obtener los encodings de los rostros almacenados y capturados
            concidencia = compare_faces(f"static/captures/faces/{usuarioBD}", f"{imagen_capturada_url}")

            if concidencia > 95:
                messagebox.showinfo("Acceso concedido", f"Acceso concedido. Confianza: {concidencia:.2f}")
                
                # Borrar la imagen capturada porque la verificación fue exitosa
                os.remove(imagen_capturada_url)
                print(f"Imagen {imagen_capturada_url} borrada tras verificación exitosa")
            else:
                messagebox.showerror("Acceso denegado", "Los rostros no coinciden. Imagen guardada para revisión.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la validación: {str(e)}")
    else:
        messagebox.showerror("Error", "Usuario no encontrado")
# Crear la tabla de usuarios si no existe
crear_tabla_usuarios()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Sistema de Autenticación")

label_usuario = tk.Label(root, text="Usuario:")
label_usuario.pack()
entry_usuario = tk.Entry(root)
entry_usuario.pack()

label_contrasena = tk.Label(root, text="Contraseña:")
label_contrasena.pack()
entry_contrasena = tk.Entry(root, show="*")
entry_contrasena.pack()

btn_iniciar_sesion = tk.Button(root, text="Iniciar sesión", command=iniciar_sesion_admin)
btn_iniciar_sesion.pack()

btn_validar_identidad = tk.Button(root, text="Validar Identidad", command=validar_identidad)
btn_validar_identidad.pack()

root.mainloop()
