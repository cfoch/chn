from django.db import models

from usuarios.models import Usuario


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuarios = models.ManyToManyField(Usuario, through='Inscripcion')

    def __str__(self):
        return self.titulo


class Inscripcion(models.Model):
    class Meta:
        unique_together = [
            ['usuario', 'curso']
        ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
