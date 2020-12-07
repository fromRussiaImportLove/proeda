from django import template
from random import choice

from django.urls import reverse

from recipes.models import Basket, Favorite, Follow, Recipe

register = template.Library()


@register.filter
def is_basked(user, recipe):
    return Basket.objects.is_basked(recipe, user)


@register.filter
def is_favorite(user, recipe):
    return Favorite.objects.is_follow(recipe, user)


@register.filter
def is_follow(user, author):
    return Follow.objects.is_follow(author, user)


@register.filter
def checked(arg):
    return 'checked' if arg else None


@register.filter
def random_recipe():
    url = reverse('recipe')
    recipe_id = choice(Recipe.objects.values('id'))['id']
    recipe = Recipe.objects.get(id=recipe_id)
    return url + recipe_id + recipe.slug
