import logging
import django.db.models.deletion
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from django.db import migrations, models


logger = logging.getLogger(__name__)


def normalizar_curso_usuarios(apps, schema_editor):
    Progreso = apps.get_model('videos', 'Progreso')
    Inscripcion = apps.get_model('cursos', 'Inscripcion')
    # Evitar caching.
    progresos = Progreso.objects.all().iterator()

    for progreso in progresos:
        inscripcion = Inscripcion.objects.filter(curso=progreso.curso,
                                                 usuario=progreso.usuario).first()
        if not inscripcion:
            logger.warning('Inconsistencia en base de datos procesando Progreso.id=%d',
                           progreso.id)
            continue

        # Como el documento menciona: relacionar la tabla "Progreso de video" a la tabla
        # "inscripción" y a la categoria del curso.
        progreso.inscripcion = inscripcion
        progreso.curso_categoria = progreso.curso.categoria
        progreso.save()


def denormalizar_curso_usuarios(apps, schema_editor):
    Progreso = apps.get_model('videos', 'Progreso')
    progresos = Progreso.objects.all().iterator()
    for progreso in progresos:
        progreso.curso = progreso.inscripcion.curso
        progreso.usuario = progreso.inscripcion.usuario
        progreso.save()


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='progreso',
            name='inscripcion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cursos.Inscripcion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='progreso',
            name='curso_categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cursos.Categoria'),
            preserve_default=False,
        ),
        migrations.RunPython(normalizar_curso_usuarios, denormalizar_curso_usuarios),
        migrations.AlterField(
            model_name='progreso',
            name='inscripcion',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='cursos.Inscripcion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='progreso',
            name='curso_categoria',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='cursos.Categoria'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='progreso',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='progreso',
            name='usuario',
        ),
    ]
