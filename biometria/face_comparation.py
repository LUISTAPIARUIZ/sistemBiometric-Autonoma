import boto3

# Configura tus credenciales de AWS
aws_access_key_id = 'AKIA4MTWIQDHRXLQDMPH'
aws_secret_access_key = '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'
region_name = 'us-west-2'  # Cambia a tu región si es necesario

# Inicializa el cliente de Rekognition
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

def compare_faces(source_image_path, target_image_path):
    with open(source_image_path, 'rb') as source_image_file:
        source_image_bytes = source_image_file.read()

    with open(target_image_path, 'rb') as target_image_file:
        target_image_bytes = target_image_file.read()

    response = rekognition.compare_faces(
        SourceImage={'Bytes': source_image_bytes},
        TargetImage={'Bytes': target_image_bytes}
    )
    
    # Verifica si hay coincidencias en FaceMatches
    if 'FaceMatches' in response and len(response['FaceMatches']) > 0:
        # Accede al primer elemento de las coincidencias y extrae el valor de confianza
        confidence = response['FaceMatches'][0]['Similarity']
        return confidence
    else:
        # Si no hay coincidencias, devuelve 0 o algún valor para indicar que no hay match
        return 0
