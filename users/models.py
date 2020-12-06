from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    is_banned = models.BooleanField('banned', default=False)
    role = models.CharField(
        max_length=200,
        default=Roles.USER,
        choices=Roles.choices,
    )

    def fullname(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'.strip()
        else:
            return f'user: {self.username}'
