from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import status  
from rest_framework.decorators import api_view
from datetime import datetime
from MyDocumentsApp.ProcesarImagenes.easyocr.easyocr_frontal import *
from MyDocumentsApp.ProcesarImagenes.easyocr.easyocr_reverso import *

@api_view(['POST'])
def  peticioneasyocr(request):
    
    if 'imagen_reverso' not in request.FILES or 'imagen_anverso' not in request.FILES:

        return Response({"mensaje": "Ambas imágenes son requeridas"}, status=status.HTTP_400_BAD_REQUEST)
    
    imagenes_dir = os.path.join(settings.MEDIA_ROOT, 'documentos')
    os.makedirs(imagenes_dir, exist_ok=True)

      # Obtener las imágenes enviadas
    imagen_reverso = request.FILES['imagen_reverso']
    imagen_anverso = request.FILES['imagen_anverso']

    # Guardar las imágenes en el servidor
    img_reverso_path = os.path.join(imagenes_dir, f'reverso_easy_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg')
    img_anverso_path = os.path.join(imagenes_dir, f'anverso_esasy_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg')

    # Guardar las imágenes en el sistema de archivos
    with open(img_reverso_path, 'wb') as f:
        for chunk in imagen_reverso.chunks():
            f.write(chunk)

    with open(img_anverso_path, 'wb') as f:
        for chunk in imagen_anverso.chunks():
            f.write(chunk)

    repuesta_opcion = True
    texto = ''
    textolimpio = ''
    numerodocumento = ''
    sexo = ''
    fecha_vencimiento = datetime.now()
    estado = ''
    nombres = ''
    apellidos = ''
    fecha_nacimiento = ''
    tipo = ''

    # llamada a funcion que extrae los datos de la parte frontal
    data_data_frontal = easyocr_frontal(img_reverso_path)
    
    texto_anverso=data_data_frontal['texto_imagen']
    sexo_anv=data_data_frontal['sexo_front']
    fecha_vencimiento_anv=data_data_frontal['fecha_vencimiento_front']
    nombres_anv=data_data_frontal['nombres_front']
    apellidos_anv=data_data_frontal['apellidos_front']
    fecha_nacimiento_anv=data_data_frontal['fecha_nacimiento_front']
    respuesta_anverso = {
                "mensaje": "Datos extraídos exitosamente",
                "Texto Original": texto_anverso,
                "valores": {
                    "Sexo": sexo_anv,
                    "Fecha Vencimiento": fecha_vencimiento_anv,
                    "Nombres": nombres_anv,
                    "Apellidos": apellidos_anv,
                    "Fecha Nacimiento": fecha_nacimiento_anv
                }
            }



    # llamada a funcion que extrae los datos del reverso
    data_data_reverso = easyocr_reverso(img_reverso_path)
    mensaje= "Datos extraídos exitosamente"
    texto=data_data_reverso['texto_imagen']
    textolimpio=data_data_reverso['texto_sin_espacios'],
    numerodocumento=data_data_reverso['numero_documento_res'] 
    sexo=data_data_reverso['sexo_resp']
    fecha_vencimiento=data_data_reverso['fecha_vencimiento_resp']
    estado=data_data_reverso['estado_resp']
    nombres=data_data_reverso['nombres_resp']
    apellidos=data_data_reverso['apellidos_resp']
    fecha_nacimiento=data_data_reverso['fecha_nacimiento_resp']

    respuesta_reverso = {
            "mensaje": mensaje,
            "datos": textolimpio,
            "Texto Original": texto,
            "tipo":tipo,
            "valores": {
                "Numero Cedula": numerodocumento,
                "Sexo": sexo,
                "Fecha Vencimiento": fecha_vencimiento,
                "Estado": estado,
                "Nombres": nombres,
                "Apellidos": apellidos,
                "Fecha Nacimiento": fecha_nacimiento
            }
        }
    
    respuesta = {
                'reverso': respuesta_reverso,
                'anverso': respuesta_anverso
            }
    

    try:
        os.remove(img_reverso_path)
        os.remove(img_anverso_path)
    except OSError as e:
         pass
    
    return Response(respuesta, status=status.HTTP_200_OK)