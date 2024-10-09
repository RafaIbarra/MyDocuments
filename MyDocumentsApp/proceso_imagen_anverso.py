import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
def validar_fecha(fecha_texto):
    try:
        # Intentar convertir la fecha usando el formato correcto
        datetime.strptime(fecha_texto, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def anverso_opcion_uno(direccion_imagen):
    respuesta_correcta=True
    imagen = Image.open(direccion_imagen)
    imagen = imagen.convert('L')
    enhancer = ImageEnhance.Brightness(imagen)
    imagen = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Contrast(imagen)
    imagen = enhancer.enhance(2)
    imagen = imagen.filter(ImageFilter.SHARPEN)
    
    
    texto_imagen = pytesseract.image_to_string(imagen)
    texto = texto_imagen.strip()
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
        fecha_nacimiento = "No válida"
    
    if not validar_fecha(fecha_vencimiento):
        fecha_vencimiento = "No válida"

    sexo = sexo[0].upper() if sexo else "No encontrado"

    return texto_imagen,sexo,fecha_vencimiento,nombres,apellidos,fecha_nacimiento