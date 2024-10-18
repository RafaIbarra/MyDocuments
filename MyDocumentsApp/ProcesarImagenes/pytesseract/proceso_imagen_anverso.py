import os
from django.conf import settings
import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'D:\Programas\tesseract.exe'
def validar_fecha(fecha_texto):
    try:
        # Intentar convertir la fecha usando el formato correcto
        datetime.strptime(fecha_texto, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def anverso_opcion_uno(direccion_imagen):
    respuesta_correcta=True
    error_formato=False
    mensaje_deteccion='No detectada correctamente'
    texto_imagen=''
    sexo=''
    fecha_vencimiento=''
    nombres=''
    apellidos=''
    fecha_nacimiento=''

    imagen = Image.open(direccion_imagen)
    imagen = imagen.convert('L')
    enhancer = ImageEnhance.Brightness(imagen)
    imagen = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Contrast(imagen)
    imagen = enhancer.enhance(2)
    imagen = imagen.filter(ImageFilter.SHARPEN)
    
    print('OPCION UNO')
    texto_imagen = pytesseract.image_to_string(imagen)
    print(texto_imagen)
    texto = texto_imagen.strip()
    #if not texto.startswith("APELLIDOS, NOMBRES"):
    #    error_formato = True

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


def anverso_opcion_dos(direccion_imagen):
    respuesta_correcta=True
    error_formato=False
    mensaje_deteccion='No detectada correctamente'
    texto_imagen=''
    sexo=''
    fecha_vencimiento=''
    nombres=''
    apellidos=''
    fecha_nacimiento=''

    imagen = Image.open(direccion_imagen)
    
    # Convertir la imagen a escala de grises
    imagen = imagen.convert('L')

    
    

    # # Aumentar el brillo
    enhancer = ImageEnhance.Brightness(imagen)
    imagen = enhancer.enhance(2)  # Ajustar el nivel de brillo (puedes probar con diferentes valores)
    

    # # Aumentar el contraste
    enhancer = ImageEnhance.Contrast(imagen)
    imagen = enhancer.enhance(3)  # Ajustar el nivel de contraste
    

    # # Aplicar filtro para mejorar los bordes y nitidez
    imagen = imagen.filter(ImageFilter.SHARPEN)

    

    # # Aplicar binarización (umbralización) para mejorar el contraste
    threshold_value = 128  # Valor de umbral (ajustable)
    imagen = imagen.point(lambda p: p > threshold_value and 255)
    

    # # Aplicar un filtro para reducir el ruido (opcional)
    imagen = imagen.filter(ImageFilter.MedianFilter(size=3))  # Filtro de Mediana para suavizar la imagen

    # # Aumentar la resolución (opcional si el texto está borroso)
    imagen = imagen.resize((imagen.width * 2, imagen.height * 2), Image.Resampling.LANCZOS)

    texto_imagen = pytesseract.image_to_string(imagen)
    print('Aumentar la resolución: ',texto_imagen)
    print('*************---------------***************------------************')




    # Definir la región de interés (opcional, ajusta los valores de acuerdo a tu imagen)
    # Puedes comentar esto si deseas procesar toda la imagen

    
    # imagen.save('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/imagen_procesada.jpg')
    imagen.save('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/imagen_procesada.jpg')

    #Region Para Apellido
    ancho, alto = imagen.size
    left = 750
    # top = 0
    top = 470
    # right = ancho // 2  # Mitad del ancho
    right = 1600  # Mitad del ancho
    # bottom = alto
    bottom = 600
    # left, top, right, bottom = 100, 50, 500, 200  # Coordenadas del área donde está el texto
    region_interes = imagen.crop((left, top, right, bottom))

    # Configurar Tesseract con el modo de segmentación de páginas
    config = '--psm 4'  # PSM 6: bloques uniformes de texto (puedes probar otros valores)

    # Extraer el texto de la imagen (o de la región de interés)
    texto_imagen = pytesseract.image_to_string(region_interes , config=config)
    print('El Apellido es:')
    print(texto_imagen)
    texto = texto_imagen.strip()
    
    # img_region = os.path.join('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/', f'region_apellido_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    # img_region = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_apellido_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    img_region = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_apellido_left-{left}_top-{top}_bottom-{bottom}_right-{right}.jpg')
    region_interes.save(img_region)

    # Region Nombre
    left = 750
    # top = 0
    top = 640
    # right = ancho // 2  # Mitad del ancho
    right = 1600  # Mitad del ancho
    # bottom = alto
    bottom = 720
    # left, top, right, bottom = 100, 50, 500, 200  # Coordenadas del área donde está el texto
    region_interes_nombres = imagen.crop((left, top, right, bottom))

    # Configurar Tesseract con el modo de segmentación de páginas
    config = '--psm 4'  # PSM 6: bloques uniformes de texto (puedes probar otros valores)

    # Extraer el texto de la imagen (o de la región de interés)
    texto_imagen_nombres = pytesseract.image_to_string(region_interes_nombres , config=config)
    print('El Nombre:')
    print(texto_imagen_nombres)
    texto = texto_imagen.strip()
    
    # img_region_nombre = os.path.join('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/', f'region_nombres_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    
    img_region_nombre = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_nombre_left-{left}_top-{top}_bottom-{bottom}_right-{right}.jpg')
    region_interes_nombres.save(img_region_nombre)


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
    region_interes = imagen.crop((left, top, right, bottom))

    # Configurar Tesseract con el modo de segmentación de páginas
    config = '--psm 4'  # PSM 6: bloques uniformes de texto (puedes probar otros valores)

    # Extraer el texto de la imagen (o de la región de interés)
    texto_imagen = pytesseract.image_to_string(region_interes , config=config)
    print('Fecha Nacimiento es:')
    print(texto_imagen)
    texto = texto_imagen.strip()
    
    # img_region = os.path.join('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/', f'region_apellido_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    # img_region = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_apellido_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    img_region = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_nacimiento_left-{left}_top-{top}_bottom-{bottom}_right-{right}.jpg')
    region_interes.save(img_region)


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
    region_interes = imagen.crop((left, top, right, bottom))

    # Configurar Tesseract con el modo de segmentación de páginas
    config = '--psm 4'  # PSM 6: bloques uniformes de texto (puedes probar otros valores)

    # Extraer el texto de la imagen (o de la región de interés)
    texto_imagen = pytesseract.image_to_string(region_interes , config=config)
    print('Numero cedula es:')
    print(texto_imagen)
    texto = texto_imagen.strip()
    
    # img_region = os.path.join('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/', f'region_apellido_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    # img_region = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_apellido_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    img_region = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_cedula_left-{left}_top-{top}_bottom-{bottom}_right-{right}.jpg')
    region_interes.save(img_region)

     #Region vencimiento
    ancho, alto = imagen.size
    left = 1600
    # top = 0
    top = 450
    # right = ancho // 2  # Mitad del ancho
    print('ancho es ', ancho)
    right = 1950  # Mitad del ancho
    # bottom = alto
    bottom = 600
    # left, top, right, bottom = 100, 50, 500, 200  # Coordenadas del área donde está el texto
    region_interes = imagen.crop((left, top, right, bottom))

    # Configurar Tesseract con el modo de segmentación de páginas
    config = '--psm 4'  # PSM 6: bloques uniformes de texto (puedes probar otros valores)

    # Extraer el texto de la imagen (o de la región de interés)
    texto_imagen = pytesseract.image_to_string(region_interes , config=config)
    print('El vencimiento es:')
    print(texto_imagen)
    texto = texto_imagen.strip()
    
    # img_region = os.path.join('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/', f'region_apellido_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    # img_region = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_apellido_{'left-',left,'top-',top, 'bottom-',bottom ,'right-',right}.jpg')
    img_region = os.path.join('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/', f'region_vencimiento_left-{left}_top-{top}_bottom-{bottom}_right-{right}.jpg')
    region_interes.save(img_region)


    

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