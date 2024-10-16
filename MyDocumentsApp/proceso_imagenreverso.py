import pytesseract
import cv2
import re
from datetime import datetime
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'D:\Programas\tesseract.exe'
mensaje_deteccion='No detectada correctamente'

def reverso_opcion_uno(direccion_imagen):
        
        
        seccion_1 =''
        seccion_2 =''
        seccion_3 =''
        tipo_opcion='OPCION UNO'
        sexo_resp = ""
        fecha_vencimiento_resp=datetime.now()
        estado_resp='S/n'
        nombres_resp=''
        apellidos_resp=''
        fecha_nacimiento_resp=datetime.now()
        numero_documento_res=''
        texto_sin_espacios=''
        
        respuesta_correcta=True
        imagen = Image.open(direccion_imagen)
        imagen = imagen.convert('L')
        enhancer = ImageEnhance.Brightness(imagen)
        imagen = enhancer.enhance(1.5)
        enhancer = ImageEnhance.Contrast(imagen)
        imagen = enhancer.enhance(2)
        imagen = imagen.filter(ImageFilter.SHARPEN)
        
        
        texto_imagen = pytesseract.image_to_string(imagen)
        
        patron = r"IDPRY.*"
        resultado = re.search(patron, texto_imagen, re.DOTALL)
        #print('texto original')
        #print(texto_imagen)

        # Si encuentra una coincidencia, extrae el texto
        if resultado:
            error_formato=False
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
                respuesta_correcta=False

            if seccion_1:
                numero_documento_res=seccion_1[5:12]
                numero_documento_res = numero_documento_res.replace('S', '5').replace('O', '9').replace('T', '7').replace('B', '8')

                if numero_documento_res.isdigit():
                    numero_documento_res = int(numero_documento_res)
                else:
                    respuesta_correcta=False
                    numero_documento_res = numero_documento_res

            if seccion_2:
                sexo_resp=seccion_2[7]
                if sexo_resp in ['M', 'F']:
                    sexo_resp=sexo_resp
                else:
                    sexo_resp = mensaje_deteccion
                    respuesta_correcta=False
                datovencimiento = seccion_2[8:14]
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


                datonacimiento = seccion_2[0:6]
                try:
                    # Convertir a int
                    anio = int("19" + datonacimiento[:2])  # '33' -> '2033'
                    mes = int(datonacimiento[2:4])  # '09'
                    dia = int(datonacimiento[4:6])  # '27'

                    # Verificar si los valores de mes y día son válidos
                    if 1 <= mes <= 12 and 1 <= dia <= 31:
                        fecha_nacimiento_resp = datetime(anio, mes, dia)
                        fecha_nacimiento_resp=fecha_nacimiento_resp.strftime('%Y-%m-%d')

                    else:
                        fecha_nacimiento_resp = mensaje_deteccion
                        respuesta_correcta=False
                    
                except ValueError:
                    # Si falla la conversión a entero, asignar 'No válido'
                    fecha_nacimiento_resp = mensaje_deteccion
                    respuesta_correcta=False
            
            if seccion_3:
                patron_nombres_apellidos = r"([A-Z<]+)<<"
                match = re.search(patron_nombres_apellidos, seccion_3)
                
                if match:
                    nombres_apellidos_seccion = match.group(1)  # IBARRA<MARTINEZ<<BLAS<RAFAEL<<
                    
                    # Separar por los << dobles
                    partes = nombres_apellidos_seccion.split('<<')

                    if len(partes) >= 2:
                        # Apellidos están en la primera parte separados por < simple
                        apellidos_resp = partes[0].replace('<', ' ').strip()  # Reemplazar < por espacio
                        # Nombres están en la última parte
                        nombres_resp = partes[1].replace('<', ' ').strip()  # Reemplazar < por espacio
                    else:
                        apellidos_resp = "No se encontraron apellidos"
                        nombres_resp = "No se encontraron nombres"
                        respuesta_correcta=False
                else:
                    apellidos_resp = "No se encontraron apellidos"
                    nombres_resp = "No se encontraron nombres"
                    respuesta_correcta=False

        else:
            error_formato=False

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


def reverso_opcion_dos(direccion_imagen):
    seccion_1 =''
    seccion_2 =''
    seccion_3 =''
    
    sexo_resp = ""
    fecha_vencimiento_resp=datetime.now()
    estado_resp='S/n'
    nombres_resp=''
    apellidos_resp=''
    fecha_nacimiento_resp=datetime.now()
    numero_documento_res=''
    tipo_opcion='OPCION DOS'
    respuesta_correcta=True
    texto_sin_espacios=''

    imagen = cv2.imread(direccion_imagen)

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    gris = cv2.convertScaleAbs(gris, alpha=1.5, beta=0)
    desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)
    _, binarizada = cv2.threshold(desenfoque, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite('E:/SGCapiataFuente/Python/MyDocuments/Backends/MyDocuments/Documentos/binarizada.jpg', binarizada)
    imagen_pil = Image.fromarray(binarizada)
    custom_config = r'--oem 3 --psm 6'
    texto_imagen = pytesseract.image_to_string(imagen_pil, config=custom_config)
    
    
    

    
    patron = r"IDPRY.*"
    resultado = re.search(patron, texto_imagen, re.DOTALL)


    # Si encuentra una coincidencia, extrae el texto
    if resultado:
        error_formato=False
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
            respuesta_correcta=False

        if seccion_1:
            numero_documento_res=seccion_1[5:12]
            numero_documento_res = numero_documento_res.replace('S', '5').replace('O', '9').replace('T', '7').replace('B', '8')

            if numero_documento_res.isdigit():
                numero_documento_res = int(numero_documento_res)
                
            else:
                respuesta_correcta=False
                numero_documento_res = numero_documento_res

        if seccion_2:
            sexo_resp=seccion_2[7]
            if sexo_resp in ['M', 'F']:
                sexo_resp=sexo_resp
            else:
                sexo_resp = mensaje_deteccion
                respuesta_correcta=False
            datovencimiento = seccion_2[8:14]
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


            datonacimiento = seccion_2[0:6]
            try:
                # Convertir a int
                anio = int("19" + datonacimiento[:2])  # '33' -> '2033'
                mes = int(datonacimiento[2:4])  # '09'
                dia = int(datonacimiento[4:6])  # '27'

                # Verificar si los valores de mes y día son válidos
                if 1 <= mes <= 12 and 1 <= dia <= 31:
                    fecha_nacimiento_resp = datetime(anio, mes, dia)
                    fecha_nacimiento_resp=fecha_nacimiento_resp.strftime('%Y-%m-%d')

                else:
                    fecha_nacimiento_resp = mensaje_deteccion
                    respuesta_correcta=False
                
            except ValueError:
                # Si falla la conversión a entero, asignar 'No válido'
                fecha_nacimiento_resp = mensaje_deteccion
                respuesta_correcta=False
        
        if seccion_3:
            patron_nombres_apellidos = r"([A-Z<]+)<<"
            match = re.search(patron_nombres_apellidos, seccion_3)
            
            if match:
                nombres_apellidos_seccion = match.group(1)  # IBARRA<MARTINEZ<<BLAS<RAFAEL<<
                
                # Separar por los << dobles
                partes = nombres_apellidos_seccion.split('<<')

                if len(partes) >= 2:
                    # Apellidos están en la primera parte separados por < simple
                    apellidos_resp = partes[0].replace('<', ' ').strip()  # Reemplazar < por espacio
                    # Nombres están en la última parte
                    nombres_resp = partes[1].replace('<', ' ').strip()  # Reemplazar < por espacio
                else:
                    apellidos_resp = "No se encontraron apellidos"
                    nombres_resp = "No se encontraron nombres"
                    respuesta_correcta=False
            else:
                apellidos_resp = "No se encontraron apellidos"
                nombres_resp = "No se encontraron nombres"
                respuesta_correcta=False

    else:
        error_formato=True
            
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

