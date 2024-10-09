from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
# pytesseract.pytesseract.tesseract_cmd = r'D:\Programas\tesseract.exe'
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from .proceso_imagenreverso import *
from .proceso_imagen_anverso import *
# Create your views here.
class OCRView(APIView):
    def get(self, request):
        
            sexo = "No se encontró el sexo"
            fecha_vencimiento=datetime.now()
            estado='S/n'
            nombres=''
            apellidos=''
            nueva_seccion=''
        # Procesar la imagen con Tesseract OCR
            imagen = Image.open('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/20241005_212030.jpg')
            texto_extraido = pytesseract.image_to_string(imagen)

            
            patron = r"IDPRY.*"
            resultado = re.search(patron, texto_extraido, re.DOTALL)


            # Si encuentra una coincidencia, extrae el texto
            if resultado:
                texto_resultado = resultado.group(0)
                texto_sin_espacios = re.sub(r'[ \t]+', ' ', texto_resultado)
                texto_sin_espacios = re.sub(r'(?<=\w) +(?=<<)', '', texto_sin_espacios)
                print('texto_sin_espacios: ',texto_sin_espacios)
                patron_numero_documento = r"IDPRY(\d+)<<"
                numero_documento = re.search(patron_numero_documento, texto_sin_espacios)
                if numero_documento:
                    numero_documento = numero_documento.group(1)
                else:
                    numero_documento = "No se encontró el número de documento"

                patron_codigo_unidad = r"<<(\d+)<<"
                codigo_unidad = re.search(patron_codigo_unidad, texto_sin_espacios)

                if codigo_unidad:
                    codigo_unidad = codigo_unidad.group(1)
                else:
                    codigo_unidad = "No se encontró el código de unidad"

                # Extraer la sección desde el primer valor después del código de unidad
                
                patron_seccion = r"<<\d+(\D*\d+.*)"  # << seguido de dígitos, luego capturamos lo que sigue, incluyendo saltos de línea
                seccion = re.search(patron_seccion, texto_sin_espacios, re.DOTALL)  # re.DOTALL permite capturar saltos de línea

                if seccion:
                    nueva_seccion = seccion.group(1).strip()  # Eliminar espacios en blanco al principio y al final

                    # Eliminar los primeros caracteres < y el primer tabulador o espacio
                    nueva_seccion = re.sub(r'^[<\s]+', '', nueva_seccion)

                    # Obtener el sexo en la posición 7 (suponiendo que la posición empieza en 0)
                    if len(nueva_seccion) > 7:
                        sexo = nueva_seccion[7]
                    
                        

                    print("Nueva Sección Completa: ", nueva_seccion)
                    print("Sexo: ", sexo)
                    if len(nueva_seccion) > 14:  # Verificamos que haya suficientes caracteres
                        vencimiento = nueva_seccion[8:14]
                        anio = int("20" + vencimiento[:2])  # '33' -> '2033'
                        mes = int(vencimiento[2:4])  # '09'
                        dia = int(vencimiento[4:6])  # '27'

                        # Crear la fecha de vencimiento
                        fecha_vencimiento = datetime(anio, mes, dia)
                        fecha_actual = datetime.now()
                        if fecha_vencimiento > fecha_actual:
                            estado = "Activo"
                        else:
                            estado = "Vencido"
                    else:
                        vencimiento = "No se encontró el vencimiento"
                        estado = "Desconocido"

                    patron_nombres_apellidos = r"\n([A-Z<]+)<<"
                    match = re.search(patron_nombres_apellidos, nueva_seccion)

                    if match:
                        nombres_apellidos_seccion = match.group(1)  # IBARRA<MARTINEZ<<BLAS<RAFAEL<<
                        
                        # Separar por los << dobles
                        partes = nombres_apellidos_seccion.split('<<')

                        if len(partes) >= 2:
                            # Apellidos están en la primera parte separados por < simple
                            apellidos = partes[0].replace('<', ' ').strip()  # Reemplazar < por espacio
                            # Nombres están en la última parte
                            nombres = partes[1].replace('<', ' ').strip()  # Reemplazar < por espacio
                        else:
                            apellidos = "No se encontraron apellidos"
                            nombres = "No se encontraron nombres"
                    else:
                        apellidos = "No se encontraron apellidos"
                        nombres = "No se encontraron nombres"

                    print("Apellidos: ", apellidos)
                    print("Nombres: ", nombres)

                respuesta = {
                    "mensaje": "Datos extraídos exitosamente",
                    "datos": texto_sin_espacios,
                    "valores": {
                        "numero_documento": numero_documento,
                        "codigo_unidad": codigo_unidad,
                        "sexo": sexo,
                        "vencimiento": fecha_vencimiento.strftime('%Y-%m-%d'),
                        "Estado": estado,
                        "Nombres": nombres,
                        "Apellidos": apellidos,
                        "restante":nueva_seccion
                    }
                }
                return Response(respuesta, status=status.HTTP_200_OK)
            else:
               return Response({"mensaje": "No se encontró el texto"}, status=status.HTTP_400_BAD_REQUEST)

            

class OCRView2(APIView):
    def get(self, request):
        sexo = ""
        fecha_vencimiento=datetime.now()
        estado='S/n'
        nombres=''
        apellidos=''
        sexo=''
        estado=''
        apellidos = "No se encontraron apellidos"
        nombres = "No se encontraron nombres"
        repuesta_opcion=True
        # Procesar la imagen con Tesseract OCR
        # imagen = Image.open('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/20241005_212030.jpg')
        # imagen = Image.open('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/20241005_212030.jpg')
        # imagen = Image.open('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/20241005_220402.jpg')
        img='D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/20241005_212030.jpg'
        repuesta_opcion,texto,textolimpio,numerodocumento,sexo,fecha_vencimiento,estado,nombres,apellidos,fecha_nacimiento,tipo=reverso_opcion_uno(img)
        if repuesta_opcion==False:
            repuesta_opcion,texto,textolimpio,numerodocumento,sexo,fecha_vencimiento,estado,nombres,apellidos,fecha_nacimiento,tipo=reverso_opcion_dos(img)
        # repuesta_opcion=reverso_opcion_uno('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/20241005_220402.jpg')
        if repuesta_opcion :
            respuesta_reverso = {
                "mensaje": "Datos extraídos exitosamente",
                "datos": textolimpio,
                "Texto Original":texto,
                "Respuesta":repuesta_opcion,
                "Tipo": tipo,
                "valores": {
                    
                    "Numero Cedula": numerodocumento,
                    "Sexo": sexo,
                    "Fecha Vencimiento":fecha_vencimiento,
                    "Estado": estado,
                    "Nombres":nombres,
                    "Apellidos":apellidos,
                    "Fecha Nacimiento": fecha_nacimiento

                }
            }
            #return Response(respuesta_reverso, status=status.HTTP_200_OK)
    
        else:
             respuesta_reverso = {
                "mensaje": "No se pudo encontrar los datos el texto",
                "datos": textolimpio,
                "Texto Original":texto,
                
            }
        img_anverso='D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/20241005_222825.jpg'
        texto_anverso,sexo_anv,fecha_vencimiento_anv,nombres_anv,apellidos_anv,fecha_nacimiento_anv=anverso_opcion_uno(img_anverso)
        respuesta_anverso = {
            "mensaje": "Datos extraídos exitosamente",
            
            "Texto Original":texto_anverso,
            "valores": {
                    "Sexo": sexo_anv,
                    "Fecha Vencimiento":fecha_vencimiento_anv,
                    "Nombres":nombres_anv,
                    "Apellidos":apellidos_anv,
                    "Fecha Nacimiento": fecha_nacimiento_anv

                }
            
            
        }

        respuesta={
            'reverso':respuesta_reverso,
            'anverso':respuesta_anverso
        }

        return Response(respuesta, status=status.HTTP_200_OK)
            #  return Response(respuesta_reverso, status=status.HTTP_400_BAD_REQUEST)
            

class OCRView3(APIView):
    def get(self, request):
        
            sexo = "No se encontró el sexo"
            fecha_vencimiento=datetime.now()
            estado='S/n'
            nombres=''
            apellidos=''
        
            seccion_1 =''
            seccion_2 =''
            seccion_3 =''
            sexo=''
            
            apellidos = "No se encontraron apellidos"
            nombres = "No se encontraron nombres"
            numero_documento_corregida=''

            imagen = cv2.imread('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/20241005_220402.jpg')
            
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            gris = cv2.convertScaleAbs(gris, alpha=1.5, beta=0)
            desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)
            _, binarizada = cv2.threshold(desenfoque, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            cv2.imwrite('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/binarizada.jpg', binarizada)
            imagen_pil = Image.fromarray(binarizada)
            custom_config = r'--oem 3 --psm 6'
            texto_extraido = pytesseract.image_to_string(imagen_pil, config=custom_config)

            # gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            # desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)
            # _, binarizada = cv2.threshold(desenfoque, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # kernel = np.ones((1, 1), np.uint8)
            # binarizada_morf = cv2.morphologyEx(binarizada, cv2.MORPH_CLOSE, kernel)
            # imagen_pil = Image.fromarray(binarizada_morf)
            # enhancer = ImageEnhance.Sharpness(imagen_pil)
            # imagen_pil_nitida = enhancer.enhance(2.0)
            # contrast = ImageEnhance.Contrast(imagen_pil_nitida)
            # imagen_contraste = contrast.enhance(2)
            # imagen_grande = imagen_contraste.resize((imagen_contraste.width * 1, imagen_contraste.height * 1), Image.LANCZOS)
            # imagen_grande.save('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/imagen_agrandada_pil.jpg')
            # custom_config = r'--oem 3 --psm 4'
            # texto_extraido = pytesseract.image_to_string(imagen_grande, config=custom_config)




            patron = r"IDPRY.*"
            resultado = re.search(patron, texto_extraido, re.DOTALL)


            # Si encuentra una coincidencia, extrae el texto
            if resultado:
                texto_resultado = resultado.group(0)
                texto_sin_espacios = re.sub(r'[ \t]+', ' ', texto_resultado)
                texto_sin_espacios = re.sub(r'(?<=\w) +(?=<<)', '', texto_sin_espacios)
                secciones = texto_sin_espacios.strip().split('\n')
                
                if len(secciones) >= 3:
                    seccion_1 = secciones[0]
                    seccion_1 = re.sub(r'(?<=\w) +(?=\w)', '', seccion_1)

                    seccion_2 = secciones[1]
                    seccion_2 = re.sub(r'(?<=\w) +(?=\w)', '', seccion_2)

                    seccion_3 = secciones[2]
                    seccion_3 = re.sub(r'(?<=\w) +(?=\w)', '', seccion_3)
    
                else:
                    print("No se encontraron suficientes secciones.")
                if seccion_1:
                    numero_documento=seccion_1[5:12]
                    numero_documento_corregida = numero_documento.replace('S', '5').replace('O', '9').replace('T', '7').replace('B', '8')

                    if numero_documento_corregida.isdigit():
                        numero_documento_corregida = int(numero_documento_corregida)
                    else:
                        numero_documento_corregida = numero_documento_corregida

                if seccion_2:
                    sexo=seccion_2[7]
                    if sexo in ['M', 'F']:
                        sexo=sexo
                    else:
                        sexo = "No válido"
                    
                    datovencimiento = seccion_2[8:14]
                    try:
                        # Convertir a int
                        anio = int("20" + datovencimiento[:2])  # '33' -> '2033'
                        mes = int(datovencimiento[2:4])  # '09'
                        dia = int(datovencimiento[4:6])  # '27'

                        # Verificar si los valores de mes y día son válidos
                        if 1 <= mes <= 12 and 1 <= dia <= 31:
                            fecha_vencimiento = datetime(anio, mes, dia)
                            fecha_actual = datetime.now()
                            if fecha_vencimiento > fecha_actual:
                                estado = "Activo"
                            else:
                                estado = "Vencido"

                            fecha_vencimiento=fecha_vencimiento.strftime('%Y-%m-%d')

                        else:
                            fecha_vencimiento = "No válido"
                        
                    except ValueError:
                        # Si falla la conversión a entero, asignar 'No válido'
                        fecha_vencimiento = "No válido"
                
                if seccion_3:
                    patron_nombres_apellidos = r"([A-Z<]+)<<"
                    match = re.search(patron_nombres_apellidos, seccion_3)
                    print('match nombres: ',match)
                    if match:
                        nombres_apellidos_seccion = match.group(1)  # IBARRA<MARTINEZ<<BLAS<RAFAEL<<
                        
                        # Separar por los << dobles
                        partes = nombres_apellidos_seccion.split('<<')

                        if len(partes) >= 2:
                            # Apellidos están en la primera parte separados por < simple
                            apellidos = partes[0].replace('<', ' ').strip()  # Reemplazar < por espacio
                            # Nombres están en la última parte
                            nombres = partes[1].replace('<', ' ').strip()  # Reemplazar < por espacio
                        else:
                            apellidos = "No se encontraron apellidos"
                            nombres = "No se encontraron nombres"
                    else:
                        apellidos = "No se encontraron apellidos"
                        nombres = "No se encontraron nombres"
                    

                   

                respuesta = {
                    "mensaje": "Datos extraídos exitosamente",
                    "datos": texto_sin_espacios,
                    "Texto Original":texto_extraido,
                    "valores": {
                        "seccion_1": seccion_1,
                        "seccion_2": seccion_2,
                        "seccion_3": seccion_3,
                        "Numero Cedula": numero_documento_corregida,
                        "Sexo": sexo,
                        "vencimiento":fecha_vencimiento,
                        
                        "Estado": estado,
                        "Nombres":nombres,
                        "Apellidos":apellidos

                    }
                }
                return Response(respuesta, status=status.HTTP_200_OK)
            else:
               return Response({"mensaje": "No se encontró el texto"}, status=status.HTTP_400_BAD_REQUEST)

            
        