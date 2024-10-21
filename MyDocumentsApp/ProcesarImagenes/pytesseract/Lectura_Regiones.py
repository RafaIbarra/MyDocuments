import os
from django.conf import settings
import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


if os.name == 'nt':  # 'nt' es el identificador de Windows en Python
    pytesseract.pytesseract.tesseract_cmd = settings.DIRECCION_TESSERACT


def lectura_region(imagen,left, top, right, bottom,config_psm,nombreregion):
    path_base=settings.PATH_IMAGEN_TRANSFORMADA
    
    region_interes = imagen.crop((left, top, right, bottom))
    texto_imagen = pytesseract.image_to_string(region_interes , config=config_psm)
    texto = texto_imagen.strip()
    img_region = os.path.join(path_base, f'{nombreregion}_left-{left}_top-{top}_bottom-{bottom}_right-{right}.jpg')
    # region_interes.save(img_region)
    # print('la region :',nombreregion,' resula: ',texto)
    return texto