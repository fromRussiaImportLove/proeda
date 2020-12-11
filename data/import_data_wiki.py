import csv
from recipes.models import Recipe, Ingredient, IngredientsInRecipe
from users.models import CustomUser
from random import choice, randint


def generator_tags(random_num):
    breakfast = bool(1 & random_num)*'breakfast'
    lunch = bool(2 & random_num)*'lunch'
    dinner = bool(4 & random_num)*'dinner'

    return filter(lambda x: x, [breakfast, lunch, dinner])


def import_recipes():
    file = 'data/dishes.csv'
    authors = CustomUser.objects.all()
    times = [5, 10, 15, 20, 30, 45, 60, 90, 120]
    with open(file) as f:
        rows_counter = sum(1 for row in csv.reader(f, delimiter='\t'))
    with open(file) as f:
        reader = csv.reader(f, delimiter='\t')
        n = 1
        for row in reader:
            # import recipe from fixtures
            recipe, created = Recipe.objects.get_or_create(
                name=row[0],
                description=row[1],
                image=row[2],
                author=choice(authors),
                cooking_time=choice(times),
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
            print(f'Created {n}/{rows_counter} recipes')
            n += 1

        print('job is done')

