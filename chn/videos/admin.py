from django.contrib import admin

from .models import Progreso


@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'duracion_minutos', 'dia')
