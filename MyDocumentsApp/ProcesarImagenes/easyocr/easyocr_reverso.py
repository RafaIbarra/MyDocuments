from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
def easyocr_reverso(direccion_imagen):

    imagen = Image.open(direccion_imagen) # toma la imagen en la direccion previamente almacenada
    texto_imagen="" # texto extraido de la imagen
    sexo_resp = "" 
    fecha_vencimiento_resp=datetime.now()
    estado_resp='S/n'
    nombres_resp=''
    apellidos_resp=''
    fecha_nacimiento_resp=datetime.now()
    numero_documento_res=''
    texto_sin_espacios=''
    
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
            
        }
        
    return data_respuesta