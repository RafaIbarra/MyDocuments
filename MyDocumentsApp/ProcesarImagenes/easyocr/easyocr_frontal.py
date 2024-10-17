from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
def easyocr_frontal(direccion_imagen):

    imagen = Image.open(direccion_imagen) # toma la imagen en la direccion previamente almacenada
    texto_imagen="" # texto extraido de la imagen
    sexo_resp = "" 
    fecha_vencimiento_resp=datetime.now()
    estado_resp='S/n'
    nombres_resp=''
    apellidos_resp=''
    fecha_nacimiento_resp=datetime.now()
    
    print('aca podes hacer print para ver en la consola')
    
    
    data_respuesta={
            'texto_imagen':texto_imagen,
        
            'sexo_front':sexo_resp,
            'fecha_vencimiento_front':fecha_vencimiento_resp,
            'estado_front':estado_resp,
            'nombres_front':nombres_resp,
            'apellidos_front':apellidos_resp,
            'fecha_nacimiento_front':fecha_nacimiento_resp,
            
        }
        
    return data_respuesta