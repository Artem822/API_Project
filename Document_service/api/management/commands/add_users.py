from django.core.management.base import BaseCommand
from api.models import User, Role



class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            if not User.objects.count() and Role.objects.count() == 4:
                admin = User.objects.create(
                    username='admin',
                    email='admin@email.com',
                    is_superuser=True,
                    is_staff=True,
                )
                admin.set_password('admin')
                admin.roles.add(Role.objects.get(role='Admin'))
                admin.save()

                manager = User.objects.create(
                    username='manager',
                    email='manager@email.com',
                    is_superuser=False,
                    is_staff=False,
                    )
                manager.set_password('manager')
                manager.roles.add(Role.objects.get(role='Manager'))
                manager.save()

                doctor = User.objects.create(
                    username='doctor',
                    email='doctor@email.com',
                    is_superuser=False,
                    is_staff=False,
                    )
                doctor.set_password('doctor')
                doctor.roles.add(Role.objects.get(role='Doctor'))
                doctor.save()    
            
                user = User.objects.create(
                    username='user',
                    email='user@email.com',
                    is_superuser=False,
                    is_staff=False,
                )
                user.set_password('user')
                user.roles.add(Role.objects.get(role='User'))
                user.save()

                self.stdout.write(self.style.SUCCESS('Базовые пользователи успешно созданы'))

            else:
                self.stdout.write(self.style.WARNING('Пользователи уже существуют или роли не созданы'))


        except Exception as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при создании базовых пользователей: {str(error)}'))