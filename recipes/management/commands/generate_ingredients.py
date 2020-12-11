from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from recipes.models import Ingredient, Unit
import csv
import os


class Command(BaseCommand):
    help = 'Generate ingredients from fixtures located in data/ingredients.csv'

    csv_data = os.path.join(settings.BASE_DIR, "data/ingredients.csv")

    def handle(self, *args, **options):
        with open(self.csv_data, encoding='utf-8') as f:
            reader = csv.reader(f)
            self.stdout.write(f'{self.csv_data} opened and import begining')
            for row in reader:
                ingridient_text = row[0]
                unit_text = row[1]
                if unit_text and ingridient_text:
                    unit, _ = Unit.objects.get_or_create(name=unit_text)
                    obj, created = Ingredient.objects.get_or_create(
                        name=ingridient_text,
                        unit=unit,
                    )

            self.stdout.write(self.style.SUCCESS(
                    f'Import ingredients finished'))

