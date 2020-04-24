from django.contrib import admin

from .models import Progreso


@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'curso', 'duracion_minutos', 'dia', 'categoria', 'inscripcion')

    def usuario(self, obj):
        return str(obj.inscripcion.usuario)

    def curso(self, obj):
        return str(obj.inscripcion.curso)

    def categoria(self, obj):
        return obj.curso_categoria.nombre
