from django import template
from random import choice

from django.urls import reverse

from recipes.models import Basket, Favorite, Follow, Recipe

register = template.Library()


@register.filter
def is_in_basket(user, recipe):
    return Basket.objects.is_in_basket(recipe, user)


@register.filter
def is_favorite(user, recipe):
    return Favorite.objects.is_follow(recipe, user)


@register.filter
def is_follow(user, author):
    return Follow.objects.is_follow(author, user)


@register.filter
def checked(arg):
    return 'checked' if arg else None


@register.simple_tag
def random_recipe_url():
    recipe_id = choice(Recipe.objects.values('id'))['id']
    recipe = Recipe.objects.get(id=recipe_id)
    return recipe.get_absolute_url()
