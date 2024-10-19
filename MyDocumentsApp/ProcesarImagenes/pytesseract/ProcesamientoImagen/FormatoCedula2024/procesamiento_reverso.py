import os
import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from ...TransformacionImagen import *



def Formato_Nuevo_Reverso(direccion_imagen):
    seccion_1 =''
    seccion_2 =''
    seccion_3 =''
    texto_imagen=''
    tipo_opcion='OPCION UNO'
    sexo_resp = ""
    fecha_vencimiento_resp=datetime.now()
    estado_resp='S/n'
    nombres_resp=''
    apellidos_resp=''
    fecha_nacimiento_resp=datetime.now()
    numero_documento_res=''
    texto_sin_espacios=''
    error_formato=True
    mensaje_deteccion=''
    
    respuesta_correcta=True
    # imagen = Image.open(direccion_imagen)

    # # Convertir la imagen a escala de grises
    # imagen = imagen.convert('L')

    #  # # Aumentar el brillo
    # enhancer = ImageEnhance.Brightness(imagen)
    # imagen = enhancer.enhance(3)  # Ajustar el nivel de brillo (puedes probar con diferentes valores)
    

    # # # Aumentar el contraste
    # enhancer = ImageEnhance.Contrast(imagen)
    # imagen = enhancer.enhance(3)  # Ajustar el nivel de contraste
    

    # # # Aplicar filtro para mejorar los bordes y nitidez
    # imagen = imagen.filter(ImageFilter.SHARPEN)

    

    # # # Aplicar binarización (umbralización) para mejorar el contraste
    # threshold_value = 128  # Valor de umbral (ajustable)
    # imagen = imagen.point(lambda p: p > threshold_value and 255)
    

    # # # Aplicar un filtro para reducir el ruido (opcional)
    # imagen = imagen.filter(ImageFilter.MedianFilter(size=3))  # Filtro de Mediana para suavizar la imagen

    # # # Aumentar la resolución (opcional si el texto está borroso)
    # imagen = imagen.resize((imagen.width * 5, imagen.height * 5), Image.Resampling.LANCZOS)
    # path_base='E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/'
    # imagen.save(os.path.join(path_base,'imagen_procesada_reverso.jpg'))
    # texto_imagen = pytesseract.image_to_string(imagen)
    texto_imagen=Configuracion_inicial(direccion_imagen,'imagen_procesada_reverso.jpg')
    # print(texto_imagen)
    patron = r"INPRY.*"
    resultado = re.search(patron, texto_imagen, re.DOTALL)
    print('el resultado es: ',resultado)
    if resultado:
        texto_resultado = resultado.group(0)
        texto_sin_espacios = re.sub(r'[ \t]+', ' ', texto_resultado)
        texto_sin_espacios = re.sub(r'(?<=\w) +(?=<<)', '', texto_sin_espacios)
        texto_sin_espacios = re.sub(r'(?<=\w) +(?=<)', '', texto_sin_espacios)
        print('Sin espacios: ',texto_sin_espacios)
        secciones = texto_sin_espacios.strip().split('\n')
        print('secciones: ', secciones)
        if len(secciones) >= 3:
            seccion_1 = secciones[0]
            seccion_1 = re.sub(r'(?<=\w) +(?=\w)', '', seccion_1)
            print('seccion_1: ',seccion_1)

            seccion_2 = secciones[1]
            seccion_2 = re.sub(r'(?<=\w) +(?=\w)', '', seccion_2)
            seccion_2 = re.sub(r'\s+', '', seccion_2)
            print('seccion_2: ',seccion_2)


            seccion_3 = secciones[2]
            seccion_3 = re.sub(r'(?<=\w) +(?=\w)', '', seccion_3)
            print('seccion_3: ',seccion_3)
            if seccion_2:
                
                sexo_resp=seccion_2[7]
                print('recorte: ',sexo_resp)
                if sexo_resp in ['M', 'F']:
                    sexo_resp=sexo_resp
                else:
                    sexo_resp = mensaje_deteccion
                    respuesta_correcta=False
                    sexo_resp='sin sexo'
                datovencimiento = seccion_2[8:14]
                print('datovencimiento: ',datovencimiento)
                try:
                    # Convertir a int
                    anio = int("20" + datovencimiento[:2])  # '33' -> '2033'
                    mes = int(datovencimiento[2:4])  # '09'
                    dia = int(datovencimiento[4:6])  # '27'

                    # Verificar si los valores de mes y día son válidos
                    if 1 <= mes <= 12 and 1 <= dia <= 31:
                        fecha_vencimiento_resp = datetime(anio, mes, dia)
                        fecha_actual = datetime.now()
                        if fecha_vencimiento_resp > fecha_actual:
                            estado_resp = "Activo"
                        else:
                            estado_resp = "Vencido"

                        fecha_vencimiento_resp=fecha_vencimiento_resp.strftime('%Y-%m-%d')
                        

                    else:
                        fecha_vencimiento_resp = mensaje_deteccion
                        respuesta_correcta=False
                    
                except ValueError:
                    # Si falla la conversión a entero, asignar 'No válido'
                    fecha_vencimiento_resp = mensaje_deteccion
                    respuesta_correcta=False
            

        print('sexo_resp:', sexo_resp)
        print('fecha_vencimiento_resp:', fecha_vencimiento_resp)
            # if seccion_3:
            #     patron_nombres_apellidos = r"([A-Z<]+)<<"
                
            #     match = re.search(patron_nombres_apellidos, seccion_3)
                
            #     if match:
            #         nombres_apellidos_seccion = match.group(1)  # IBARRA<MARTINEZ<<BLAS<RAFAEL<<
                    
            #         # Separar por los << dobles
            #         # partes = nombres_apellidos_seccion.split('<<')
            #         partes = re.split(r'<<|<K<', nombres_apellidos_seccion)

            #         if len(partes) >= 2:
            #             # Apellidos están en la primera parte separados por < simple
            #             apellidos_resp = partes[0].replace('<', ' ').strip()  # Reemplazar < por espacio
            #             # Nombres están en la última parte
            #             nombres_resp = partes[1].replace('<', ' ').strip()  # Reemplazar < por espacio
            #         else:
            #             apellidos_resp = "No se encontraron apellidos"
            #             nombres_resp = "No se encontraron nombres"
            #             respuesta_correcta=False
            #     else:
            #         apellidos_resp = "No se encontraron apellidos"
            #         nombres_resp = "No se encontraron nombres"
            #         respuesta_correcta=False
            #     print('nombres_resp: ',nombres_resp)
            #     print('apellidos_resp: ',apellidos_resp)

    data_respuesta={
            'texto_imagen':texto_imagen,
            'texto_sin_espacios':texto_sin_espacios,
            'numero_documento_res':numero_documento_res,
            'sexo_resp':sexo_resp,
            'fecha_vencimiento_resp':fecha_vencimiento_resp,
            'estado_resp':estado_resp,
            'nombres_resp':nombres_resp,
            'apellidos_resp':apellidos_resp,
            'fecha_nacimiento_resp':fecha_nacimiento_resp,
            'tipo_opcion':tipo_opcion
        }
        
    return error_formato,respuesta_correcta,data_respuesta