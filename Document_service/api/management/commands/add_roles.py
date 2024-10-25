from django.core.management.base import BaseCommand
from api.models import Role

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            if Role.objects.count() == 0:
                Role.objects.create(role='Admin')
                Role.objects.create(role='Manager')
                Role.objects.create(role='Doctor')
                Role.objects.create(role='User')

                self.stdout.write(self.style.SUCCESS('Роли успешно созданы'))

        except:
            self.stdout.write(self.style.ERROR('Ошибка при создании ролей'))