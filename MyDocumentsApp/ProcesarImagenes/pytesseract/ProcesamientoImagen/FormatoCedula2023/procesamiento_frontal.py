import os
from django.conf import settings
import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from ...TransformacionImagen import *
if os.name == 'nt':  # 'nt' es el identificador de Windows en Python
    pytesseract.pytesseract.tesseract_cmd = settings.DIRECCION_TESSERACT
def validar_fecha(fecha_texto):
    try:
        # Intentar convertir la fecha usando el formato correcto
        datetime.strptime(fecha_texto, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def cedula2023_frontal_opcion_uno(direccion_imagen):
    respuesta_correcta=True
    error_formato=True
    mensaje_deteccion='No detectada correctamente'
    texto_imagen=''
    sexo=''
    fecha_vencimiento=''
    nombres=''
    apellidos=''
    fecha_nacimiento=''

    # imagen = Image.open(direccion_imagen)
    # texto_imagen = pytesseract.image_to_string(imagen)
    texto_imagen,imagen=Configuracion_frontal_2023(direccion_imagen,'frontal_2023_procesada.jpg')
    patron = r"APELLIDOS, NOMBRES.*"
    resultado = re.search(patron, texto_imagen, re.DOTALL)
    texto = texto_imagen.strip()
    
     

    if resultado :
        texto_normalizado = re.sub(r'\n+', '\n', texto.strip())
        texto_normalizado = re.sub(r'\.', '', texto_normalizado)
        
        referencias = ["APELLIDOS, NOMBRES", "FECHA DE NACIMIENTO", "LUGAR DE NACIMIENTO", "FECHA DE VENCIMIENTO", "SEXO"]
       
    
        for ref1 in referencias:
            for ref2 in referencias:
                if ref1 != ref2:
                    # Buscar dos referencias en la misma línea
                    patron_juntos = rf"{ref1} {ref2}"
                    # Verificar si existe la combinación en el texto
                    if re.search(patron_juntos, texto_normalizado):
                        
                        
                        # Reemplazar para dejar el primer punto y mover el segundo al final
                        texto_normalizado = re.sub(patron_juntos, ref1, texto_normalizado)
                        # Agregar el segundo punto al final
                        texto_normalizado = f"{texto_normalizado.strip()}\n{ref2}"
                        
                        # Buscar el texto debajo de ref1
                        patron_ref1 = rf"{ref1}\n(.+)"
                        match_ref1 = re.search(patron_ref1, texto_normalizado)
                        
                        # Buscar el texto debajo de ref2
                        patron_ref2 = rf"{ref2}\n(.+)"
                        match_ref2 = re.search(patron_ref2, texto_normalizado)
                        
                        # Procesar el texto debajo de ref1
                        if match_ref1:
                            texto_debajo_ref1 = match_ref1.group(1).strip()
                            
                            
                            # Si el texto debajo tiene dos partes separadas por espacio, lo separamos
                            if ' ' in texto_debajo_ref1:
                                primera_parte, segunda_parte = texto_debajo_ref1.split(' ', 1)
                                
                                
                                # Reemplazar el texto debajo de ref1 solo con la primera parte
                                texto_normalizado = re.sub(rf"{ref1}\n{texto_debajo_ref1}", rf"{ref1}\n{primera_parte}", texto_normalizado)
                                
                                # Agregar la segunda parte al final, después de ref2
                                texto_normalizado = f"{texto_normalizado.strip()}\n{segunda_parte}"


      
        secciones = {}
        patrones = {
        "apellidos_nombres": r"APELLIDOS, NOMBRES\n(.+)\n(.+)",
        "fecha_nacimiento": r"FECHA DE NACIMIENTO\n(.+)",
        "lugar_nacimiento": r"LUGAR DE NACIMIENTO\n(.+)",
        "fecha_vencimiento": r"FECHA DE VENCIMIENTO\n(.+)",
        "sexo": r"SEXO\n(.+)"
        }
        
        for seccion, patron in patrones.items():
            
            match = re.search(patron, texto_normalizado)
            
            if match:
                # Obtener el grupo coincidente
                valor = match.group(1).strip()
                
                # Verificar si el valor no es una de las referencias
                if valor not in referencias:
                    # Asignar el valor a la sección solo si no es otra referencia
                    secciones[seccion] = match.groups()
                else:
                    secciones[seccion] = ''
            else:
                secciones[seccion] = ''

        
        apellidos_nombres = secciones.get("apellidos_nombres", ("No encontrado", "No encontrado"))
        fecha_nacimiento = secciones.get("fecha_nacimiento", ("No encontrada",))
        lugar_nacimiento = secciones.get("lugar_nacimiento", ("No encontrado",))
        fecha_vencimiento = secciones.get("fecha_vencimiento", ("No encontrada",))
        sexo = secciones.get("sexo", ("No encontrado",))
        apellidos = apellidos_nombres[0]
        nombres = apellidos_nombres[1]
        if isinstance(fecha_nacimiento, tuple):
            fecha_nacimiento = fecha_nacimiento[0]

        if isinstance(lugar_nacimiento, tuple):
            lugar_nacimiento = lugar_nacimiento[0]

        if isinstance(fecha_vencimiento, tuple):
            fecha_vencimiento = fecha_vencimiento[0]

        if isinstance(sexo, tuple):
            sexo = sexo[0]

        if not validar_fecha(fecha_nacimiento):
            fecha_nacimiento = mensaje_deteccion
        
        if not validar_fecha(fecha_vencimiento):
            fecha_vencimiento = mensaje_deteccion

        sexo = sexo[0].upper() if sexo else mensaje_deteccion
    else:
        error_formato= False

    data_respuesta={
            'texto_imagen':texto_imagen,
            'sexo_resp':sexo,
            'fecha_vencimiento_resp':fecha_vencimiento,
            'nombres_resp':nombres,
            'apellidos_resp':apellidos,
            'fecha_nacimiento_resp':fecha_nacimiento,
            
        }

    return error_formato,data_respuesta


