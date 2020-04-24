from django.db import models

from cursos.models import Categoria
from cursos.models import Inscripcion


class Progreso(models.Model):
    duracion_minutos = models.IntegerField()
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    curso_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    dia = models.DateField()
