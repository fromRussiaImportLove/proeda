import csv
import os
from random import choice, randint

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, IngredientsInRecipe, Recipe
from users.models import CustomUser


def generator_tags(random_num):
    breakfast = bool(1 & random_num)*'breakfast'
    lunch = bool(2 & random_num)*'lunch'
    dinner = bool(4 & random_num)*'dinner'

    return filter(lambda x: x, [breakfast, lunch, dinner])


class Command(BaseCommand):
    help = 'Import recipes and mix between tags and users'

    file_ = os.path.join(settings.BASE_DIR, "data/dishes.csv")
    authors_ = CustomUser.objects.all()
    times_ = [5, 10, 15, 20, 30, 45, 60, 90, 120]

    def handle(self, *args, **options):
        with open(self.file_) as f:
            rows_count = sum(1 for row in csv.reader(f, delimiter='\t'))
        with open(self.file_) as f:
            reader = csv.reader(f, delimiter='\t')
            n = 1
            for row in reader:
                # import recipe from fixtures
                if Recipe.objects.filter(name=row[0]).exists():
                    continue
                recipe, created = Recipe.objects.get_or_create(
                    name=row[0],
                    description=row[1],
                    image=row[2],
                    author=choice(self.authors_),
                    cooking_time=choice(self.times_),
                )
                # generate tags
                tags_generate = randint(1, 7)
                recipe.tags.add(*generator_tags(tags_generate))

                # generate ingredient
                num_ingredient = randint(2, 5)
                ingredients_ids = Ingredient.objects.count()
                for _ in range(num_ingredient):
                    ing, created = IngredientsInRecipe.objects.get_or_create(
                        recipe=recipe,
                        ingredient=Ingredient.objects.get(
                            id=randint(1, ingredients_ids)),
                        amount=randint(10, 1000),
                    )
                # print status
                self.stdout.write(f'Created {n}/{rows_count} recipes {recipe}')
                n += 1

            self.stdout.write('job is done')
