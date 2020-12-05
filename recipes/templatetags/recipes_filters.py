from django import template
from recipes.models import Basket, Favorite, Follow

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
