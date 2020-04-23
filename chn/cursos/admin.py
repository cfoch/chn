from django.contrib import admin

from .models import Categoria
from .models import Curso
from .models import Inscripcion


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso')


for model in (Categoria, Curso):
    admin.site.register(model)
