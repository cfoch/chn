from faker import Faker
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    DEFAULT_PASSWORD = 'pass'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fake = Faker()
        self.n_usuarios = 30

    def poblar_usuarios(self):
        insertions = 0
        while insertions < self.n_usuarios:
            email = self._fake.email()
            user_model = get_user_model()

            if not user_model.objects.filter(email=email).exists():
                usuario = user_model.objects.create_user(email, password=self.DEFAULT_PASSWORD)
                usuario.save()
                insertions += 1

    def add_arguments(self, parser):
        parser.add_argument('--n-usuarios',
                            help='La cantidad de usuarios a poblar.',
                            type=int)

    def handle(self, *args, **options):
        self.n_usuarios = options.get('n_usuarios', self.n_usuarios)

        self.poblar_usuarios()
