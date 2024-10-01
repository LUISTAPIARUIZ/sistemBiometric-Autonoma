import cv2
import os
import time

def capturar_rostro(nombre_usuario):
    # Crear carpeta 'captures' si no existe
    if not os.path.exists('static/captures/faces'):
        os.makedirs('static/captures/faces')

    # Iniciar la cámara
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Captura de Rostro")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error al acceder a la cámara")
            break
        
        # Mostrar la ventana con el feed de la cámara
        cv2.imshow("Captura de Rostro", frame)

        # Esperar a que se presione la tecla 'q' para capturar la imagen
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # Crear un nombre de archivo único usando el nombre de usuario y un timestamp
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            nombre_archivo = f'{nombre_usuario}_rostro_{timestamp}.png'

            # Guardar la imagen en la carpeta 'captures'
            ruta_completa = f'static/captures/faces/{nombre_archivo}'
            cv2.imwrite(ruta_completa, frame)
            print(f"Imagen de rostro capturada y guardada como '{ruta_completa}'")
            break

    # Cerrar la cámara y destruir la ventana
    cam.release()
    cv2.destroyAllWindows()

    # Devolver solo el nombre del archivo
    return nombre_archivo
