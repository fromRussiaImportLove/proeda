import csv
from recipes.models import Unit, Ingredient


def import_ingridients_and_units():
    file = 'data/ingredients.csv'
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            ingridient_text = row[0]
            unit_text = row[1]
            unit, _ = Unit.objects.get_or_create(name=unit_text)
            obj, created = Ingredient.objects.get_or_create(
                name=ingridient_text,
                unit=unit,
            )
        return 'ok'
