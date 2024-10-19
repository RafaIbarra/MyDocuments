import os
import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from django.conf import settings
if os.name == 'nt':  # 'nt' es el identificador de Windows en Python
    pytesseract.pytesseract.tesseract_cmd = settings.DIRECCION_TESSERACT

def Configuracion_inicial(direccion_imagen,nombrearchivotransformado):
    print('En la funcion')
    imagen = Image.open(direccion_imagen)
     # Convertir la imagen a escala de grises
    imagen = imagen.convert('L')

     # # Aumentar el brillo
    enhancer = ImageEnhance.Brightness(imagen)
    imagen = enhancer.enhance(3)  # Ajustar el nivel de brillo (puedes probar con diferentes valores)
    

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
    imagen = imagen.resize((imagen.width * 5, imagen.height * 5), Image.Resampling.LANCZOS)
    path_base=settings.PATH_IMAGEN_TRANSFORMADA
    imagen.save(os.path.join(path_base,nombrearchivotransformado))
    texto_imagen = pytesseract.image_to_string(imagen)

    return texto_imagen


def Configuracion_frontal(direccion_imagen,nombrearchivotransformado):
    print('En la funcion dos')
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
    path_base=settings.PATH_IMAGEN_TRANSFORMADA
    imagen.save(os.path.join(path_base,nombrearchivotransformado))

    texto_imagen = pytesseract.image_to_string(imagen)

    return texto_imagen,imagen