from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

USERS = [
    {'username': 'mary', 'first_name': 'Maria', 'last_name': 'Lukojo', 'email': 'fake_mary@nomail.com.fake', 'is_active': False},
    {'username': 'muzzy', 'first_name': 'Muzzy', 'last_name': 'Big Muzzy', 'email': 'fake_mazzy@nomail.com.fake', 'is_active': False},
    {'username': 'corvex', 'first_name': 'Corvex', 'last_name': '', 'email': 'fake_corvex@nomail.com.fake', 'is_active': False},
    {'username': 'JOliver', 'first_name': 'Jamie', 'last_name': 'Oliver', 'email': 'fake_joliver@nomail.com.fake', 'is_active': False},
    {'username': 'stepmom', 'first_name': 'Дорогая', 'last_name': 'Теща', 'email': 'fake_stepmom@nomail.com.fake', 'is_active': False},
    {'username': 'hblumental', 'first_name': 'Хестон', 'last_name': 'Блюменталь', 'email': 'fake_hblumental@nomail.com.fake', 'is_active': False},
    {'username': 'gorge', 'first_name': 'Гордон', 'last_name': 'Рамзи', 'email': 'fake_ramzi@nomail.com.fake', 'is_active': False},
    {'username': 'jvis', 'first_name': 'Юлия', 'last_name': 'Высоцкая', 'email': 'fake_jvis@nomail.com.fake', 'is_active': False},
]


class Command(BaseCommand):
    help = 'Generate few users from hardcoded fixtures'

    def handle(self, *args, **options):
        for user_fixture in USERS:
            user = User.objects.filter(username=user_fixture['username'])
            if user.exists():
                self.stdout.write(self.style.NOTICE(
                    f'{user.first()} already created'))
            else:
                user = User.objects.update_or_create(**user_fixture)
                self.stdout.write(self.style.SUCCESS(
                        f'{user} has been created'))
