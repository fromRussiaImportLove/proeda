# Generated by Django 3.0.11 on 2020-11-26 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20201126_0639'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IngredientsInRecipes',
            new_name='IngredientsInRecipe',
        ),
    ]
