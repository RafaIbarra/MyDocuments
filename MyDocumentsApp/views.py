from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image
import pytesseract
import re
from datetime import datetime
pytesseract.pytesseract.tesseract_cmd = r'D:\Programas\tesseract.exe'
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
            imagen = Image.open('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/20241005_212030.jpg')
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
        
            sexo = "No se encontró el sexo"
            fecha_vencimiento=datetime.now()
            estado='S/n'
            nombres=''
            apellidos=''
            nueva_seccion=''
            seccion_1 =''
            seccion_2 =''
            seccion_3 =''
        # Procesar la imagen con Tesseract OCR
            imagen = Image.open('D:/Trabajos/Proyectos/MyDocuments/Backend/MyDocumentsProject/Documentos/20241005_212030.jpg')
            texto_extraido = pytesseract.image_to_string(imagen)

            
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
                    seccion_2 = secciones[1]
                    seccion_3 = secciones[2]
                    
                    print("Sección 1: ", seccion_1)
                    print("Sección 2: ", seccion_2)
                    print("Sección 3: ", seccion_3)
                else:
                    print("No se encontraron suficientes secciones.")
                if seccion_1:
                    numero_documento=seccion_1[5:12]

                    if numero_documento.isdigit():
                        numero_documento = int(numero_documento)
                    else:
                        numero_documento = "No válido"

                respuesta = {
                    "mensaje": "Datos extraídos exitosamente",
                    "datos": texto_sin_espacios,
                    "Texto Original":texto_extraido,
                    "valores": {
                        "seccion_1": seccion_1,
                        "seccion_2": seccion_2,
                        "seccion_3": seccion_3,
                        "Numero Cedula": numero_documento

                    }
                }
                return Response(respuesta, status=status.HTTP_200_OK)
            else:
               return Response({"mensaje": "No se encontró el texto"}, status=status.HTTP_400_BAD_REQUEST)

            
        