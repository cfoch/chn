import random
import datetime
from faker import Faker
from django.core.management.base import BaseCommand

from cursos.models import Inscripcion
from videos.models import Progreso


class Command(BaseCommand):
    MAXIMAS_VISTAS_POR_VIDEO = 7
    MAXIMOS_DIAS_TRANSCURRIDOS_ENTRE_VISTA = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fake = Faker()
        self.n_progreso = 0

    def poblar_progreso(self):
        inscripciones = Inscripcion.objects.all()

        if not inscripciones:
            self.stdout.write(self.style.NOTICE('No existen inscripciones. Nada a procesar.'))

        n = 0
        while n < self.n_progreso:
            inscripcion = random.choice(inscripciones)
            usuario = inscripcion.usuario
            curso = inscripcion.curso
            maximas_vistas_por_video = random.randint(1, self.MAXIMAS_VISTAS_POR_VIDEO)
            fecha_base = datetime.date(random.randint(2018, 2020), 1, 1)
            for i in range(maximas_vistas_por_video):
                # Asumir que cada día se ve una duración proporcional y aleatoria del video.
                duracion_minutos = int(random.randint(1, 120) * (i + 1) / maximas_vistas_por_video)
                # Contar <dias_transcurridos> dias desde ultima vez que se vio el video.
                dias_transcurridos = random.randint(1, self.MAXIMOS_DIAS_TRANSCURRIDOS_ENTRE_VISTA)
                dias_transcurridos = datetime.timedelta(days=dias_transcurridos)
                fecha_base = fecha_base + dias_transcurridos
                # Guardar progreso.
                progreso = Progreso(usuario=usuario, curso=curso, dia=fecha_base, duracion_minutos=duracion_minutos)
                progreso.save()
            n += 1

    def add_arguments(self, parser):
        parser.add_argument('--n-progreso',
                            help='La cantidad de filas en la tabla progreso a poblar.',
                            type=int)

    def handle(self, *args, **options):
        self.n_progreso = options.get('n_progreso') or self.n_progreso

        self.poblar_progreso()
