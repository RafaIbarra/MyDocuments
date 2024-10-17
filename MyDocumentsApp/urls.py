from django.urls import path
from .views import *
from MyDocumentsApp.Apis.apis import *
urlpatterns = [

   path('procesar-imagen/', OCRView2.as_view(), name='procesar-imagen/'),
   path('lectura-imagen/', ViewLecturaImagen.as_view(), name='lectura-imagen/'),
   path('lectura-imagen-easy/', peticioneasyocr, name='peticioneasyocr/'),

]