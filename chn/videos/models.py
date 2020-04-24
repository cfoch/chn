from django.db import models

from cursos.models import Curso
from usuarios.models import Usuario


class Progreso(models.Model):
    duracion_minutos = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    dia = models.DateField()
