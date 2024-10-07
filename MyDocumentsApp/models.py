from django.db import models
class Documento(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    imagen = models.ImageField(upload_to='documentos/')
    procesado = models.BooleanField(default=False)
    datos_extraidos = models.TextField(blank=True, null=True)

    class Meta:
        db_table="Documento"
        
    def __str__(self):
        return f"Documento {self.id}"

# Create your models here.
