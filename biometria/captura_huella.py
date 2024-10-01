import os
import time

def capturar_huella(nombre_usuario):
    # Crear carpeta 'captures' si no existe
    if not os.path.exists('static/captures/fingerprint'):
        os.makedirs('static/captures/fingerprint')

    # Crear un nombre de archivo único para la huella
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    nombre_archivo_huella = f'{nombre_usuario}_huella_{timestamp}.dat'

    # Guardar la huella en la carpeta 'captures'
    ruta_completa = f'static/captures/fingerprint/{nombre_archivo_huella}'
    with open(ruta_completa, 'wb') as huella_file:
        # Aquí iría la captura real de la huella; estamos simulando los datos binarios
        huella_file.write(b'huella_dactilar_simulada')
        print(f"Huella capturada y guardada como '{ruta_completa}'")

    # Devolver solo el nombre del archivo de la huella
    return nombre_archivo_huella