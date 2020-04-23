import random
from faker import Faker
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cursos.models import Categoria
from cursos.models import Curso
from cursos.models import Inscripcion


class Command(BaseCommand):
    DEFAULT_PASSWORD = "pass"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fake = Faker()
        self.n_categorias = 0
        self.n_cursos = 0
        self.n_inscripciones = 0

    def poblar_categorias(self):
        categorias_nombres = set()
        while len(categorias_nombres) < self.n_categorias:
            categoria_nombre = random.choice(self._fake.catch_phrase().split()).lower()

            if categoria_nombre not in categorias_nombres:
                categoria = Categoria(nombre=categoria_nombre)
                categoria.save()
            categorias_nombres.add(categoria_nombre)

    def poblar_cursos(self):
        categorias = Categoria.objects.all()
        if not categorias:
            self.stdout.write(self.style.NOTICE('No existen categorias. Curso depende de Categoria.'))

        cursos_titulos = set()
        while len(cursos_titulos) < self.n_cursos:
            curso_titulo = self._fake.catch_phrase()
            if curso_titulo not in cursos_titulos:
                curso = Curso(titulo=curso_titulo, categoria=random.choice(categorias))
                curso.save()
            cursos_titulos.add(curso_titulo)

    def poblar_inscripciones(self):
        user_model = get_user_model()
        usuarios = user_model.objects.all()
        cursos = Curso.objects.all()

        if not usuarios:
            self.stdout.write(self.style.NOTICE('No existen usuarios. Inscripcion depende de Usuario.'))
        if not cursos:
            self.stdout.write(self.style.NOTICE('No existen cursos. Inscripcion depende de Curso.'))

        n = 0
        collisions = 0
        max_collisions = 5
        inscripciones = set()
        while n < self.n_inscripciones and collisions <= max_collisions:
            usuario = random.choice(usuarios)
            curso = random.choice(cursos)
            inscripcion = next(iter(Inscripcion.objects.filter(usuario=usuario, curso=curso)), None)
            if inscripcion is None:
                inscripciones.add((usuario, curso))
                n += 1
                collisions = 0
            else:
                collisions += 1

        if n < self.n_inscripciones:
            self.stdout.write(self.style.WARNING('Nada a insertar. No se encuentra combinaciones suficientes.'))
            return

        for usuario, curso in inscripciones:
            inscripcion = Inscripcion(usuario=usuario, curso=curso)
            inscripcion.save()

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--n-categorias',
                            help='La cantidad de categorias a poblar',
                            type=int)
        parser.add_argument('--n-cursos',
                            help='La cantidad de cursos a poblar',
                            type=int)
        parser.add_argument('--n-inscripciones',
                            help='La cantidad de inscripciones a poblar',
                            type=int)

    def handle(self, *args, **options):
        self.n_cursos = options.get('n_cursos') or self.n_cursos
        self.n_categorias = options.get('n_categorias') or self.n_categorias
        self.n_inscripciones = options.get('n_inscripciones') or self.n_inscripciones

        self.poblar_categorias()
        self.poblar_cursos()
        self.poblar_inscripciones()
