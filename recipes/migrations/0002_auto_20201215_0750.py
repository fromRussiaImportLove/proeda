# Generated by Django 3.0.11 on 2020-12-15 07:50

from django.db import migrations
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='amount',
            field=recipes.models.NonZeroPositiveSmallIntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=recipes.models.NonZeroPositiveSmallIntegerField(verbose_name='Время готовки'),
        ),
    ]
