import os
from django.conf import settings
import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from ...TransformacionImagen import *
from ...Lectura_Regiones import *

if os.name == 'nt':  # 'nt' es el identificador de Windows en Python
    pytesseract.pytesseract.tesseract_cmd = settings.DIRECCION_TESSERACT

def validar_fecha(fecha_texto):
    try:
        # Intentar convertir la fecha usando el formato correcto
        datetime.strptime(fecha_texto, "%d-%m-%Y")
        return True
    except ValueError:
        return False
    
def cedula2024_frontal_opcion_uno(direccion_imagen):
    respuesta_correcta=True
    error_formato=False
    mensaje_deteccion='No detectada correctamente'
    texto_imagen=''
    sexo=''
    fecha_vencimiento=''
    nombres=''
    apellidos=''
    fecha_nacimiento=''
    texto_imagen,imagen=Configuracion_frontal(direccion_imagen,'frontal_2024_procesada.jpg')
    
    posicion_apellidos = texto_imagen.find("APELLIDOS")
    texto_desde_apellidos=''

    if posicion_apellidos != -1:
        texto_desde_apellidos = texto_imagen[posicion_apellidos:]
        
    palabras_extraer = [
    'APELLIDOS FECHA OF VENCIMIENTO', 'APELLIDOS FECHA DE VENCIMIENTO',
    'HOMBRES DOMANTE', 'NOMBRES DOMANTE', 'ey -', '————ne',
    'LAs NACENTO', 'FECHA DE NACIMIENTO', 'LUGAR DE NACIMIENTO',
    'SEXO']
    for palabra in palabras_extraer:
    # Usamos re.escape para tratar los caracteres especiales literalmente
        texto_desde_apellidos = re.sub(re.escape(palabra), '', texto_desde_apellidos, flags=re.IGNORECASE)

    texto_desde_apellidos = re.sub(r'\n\s*\n', '\n', texto_desde_apellidos).strip()
    
    secciones = texto_desde_apellidos.strip().split('\n')
    dic_secciones = {}
    for i, seccion in enumerate(secciones, 1):  # Enumerar las secciones comenzando desde 1
        dic_secciones[f'seccion_{i}'] = seccion.strip()  # Eliminar espacios en blanco alrededor de cada sección

    # Imprimir el diccionario resultante
    
    seccion_1 = dic_secciones['seccion_1']
    partes_seccion_1 = seccion_1.split()
    patron_fecha_vencimiento = r'\d{2}-\d{2}-\d{4}'
    fecha_vencimiento = None
    apellidos = []
    for parte in partes_seccion_1:
        if re.match(patron_fecha_vencimiento, parte):
            fecha_vencimiento = parte  # Asignar la fecha cuando se encuentra el patrón
        else:
            apellidos.append(parte)  # Las palabras que no son fecha son apellidos

    # Unir los apellidos en una sola cadena
    apellidos = ' '.join(apellidos)
    

    seccion_2 = dic_secciones['seccion_2']
    partes_seccion_2 = seccion_2.split()
    nombres = ' '.join(partes_seccion_2[:-1])
    
    ##################################
    seccion_3 = dic_secciones['seccion_3']
    
    fecha_y_genero = seccion_3.split()
    fecha = fecha_y_genero[0]
    if len(fecha.split('-')[0]) == 1:  # Si el día tiene solo un dígito
        fecha = '0' + fecha
    
    seccion_3 = f"{fecha} {' '.join(fecha_y_genero[1:])}"
    
    partes_seccion_3=seccion_3.split()
    patron_fecha_nacimiento = r'\d{2}-\d{2}-\d{4}'
    fecha_nacimiento = None
    sexo = []
    for parte in partes_seccion_3:
        if re.match(patron_fecha_nacimiento, parte):
            fecha_nacimiento = parte  # Asignar la fecha cuando se encuentra el patrón
        else:
            sexo.append(parte)  # Las palabras que no son fecha son apellidos

    # Unir los apellidos en una sola cadena
    sexo = ' '.join(sexo)
    


    seccion_4 = dic_secciones['seccion_4']
    numero_cedula = re.search(r'\d+', seccion_4)
    if numero_cedula:
        numero_cedula = numero_cedula.group()
    else:
        numero_cedula = "No se encontró número de cédula"

    # Imprimir el número de cédula
    data_respuesta={
            'texto_imagen':texto_imagen,
            'sexo_resp':sexo,
            'fecha_vencimiento_resp':fecha_vencimiento,
            'nombres_resp':nombres,
            'apellidos_resp':apellidos,
            'fecha_nacimiento_resp':fecha_nacimiento,
            
        }
   
    return error_formato,data_respuesta

def cedula2024_frontal_opcion_regiones(direccion_imagen):
    respuesta_correcta=True
    error_formato=False
    mensaje_deteccion='No detectada correctamente'
    texto_imagen=''
    sexo=''
    fecha_vencimiento=''
    nombres=''
    apellidos=''
    fecha_nacimiento=''
    texto_imagen,imagen=Configuracion_frontal(direccion_imagen,'imagen_procesada.jpg')
    left = 750
    # # top = 0
    top = 470
    # # right = ancho // 2  # Mitad del ancho
    right = 1600  # Mitad del ancho
    # # bottom = alto
    bottom = 600
    # # left, top, right, bottom = 100, 50, 500, 200  # Coordenadas del área donde está el texto
    # region_interes = imagen.crop((left, top, right, bottom))

    # # Configurar Tesseract con el modo de segmentación de páginas
    config = '--psm 4'  # PSM 6: bloques uniformes de texto (puedes probar otros valores)



    texto=lectura_region(imagen,left, top, right, bottom,config,'Apellido')

    # Region Nombre
    left = 750
    # top = 0
    top = 640
    # right = ancho // 2  # Mitad del ancho
    right = 1600  # Mitad del ancho
    # bottom = alto
    bottom = 720

  

    texto=lectura_region(imagen,left, top, right, bottom,config,'Nombre')


    # Region Fecha nacimiento
    
    ancho, alto = imagen.size
    left = 750
    # top = 0
    top = 1120
    # right = ancho // 2  # Mitad del ancho
    right = 1200  # Mitad del ancho
    # bottom = alto
    bottom = 1200
    # left, top, right, bottom = 100, 50, 500, 200  # Coordenadas del área donde está el texto
    # region_interes = imagen.crop((left, top, right, bottom))

    # Configurar Tesseract con el modo de segmentación de páginas
    config = '--psm 4'  # PSM 6: bloques uniformes de texto (puedes probar otros valores)

    

    texto=lectura_region(imagen,left, top, right, bottom,config,'FechaNacimiento')


    # Region Numero cedula
    
    ancho, alto = imagen.size
    left = 290
    # top = 0
    top = 1170
    # right = ancho // 2  # Mitad del ancho
    right = 700  # Mitad del ancho
    # bottom = alto
    bottom = 1300
    # left, top, right, bottom = 100, 50, 500, 200  # Coordenadas del área donde está el texto
    # region_interes = imagen.crop((left, top, right, bottom))

    # Configurar Tesseract con el modo de segmentación de páginas
    config = '--psm 4'  # PSM 6: bloques uniformes de texto (puedes probar otros valores)

    
    texto=lectura_region(imagen,left, top, right, bottom,config,'NumeroCedula')

     #Region vencimiento
    ancho, alto = imagen.size
    left = 1600
    # top = 0
    top = 450
    # right = ancho // 2  # Mitad del ancho
    
    right = 1950  # Mitad del ancho
    # bottom = alto
    bottom = 600
 
    texto=lectura_region(imagen,left, top, right, bottom,config,'Vencimiento')

    

    if error_formato== False:
        texto_normalizado = re.sub(r'\n+', '\n', texto.strip())
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
                secciones[seccion] = match.groups()

        
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

    return error_formato,texto_imagen,sexo,fecha_vencimiento,nombres,apellidos,fecha_nacimiento
