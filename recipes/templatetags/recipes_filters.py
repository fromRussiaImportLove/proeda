from random import choice

from django import template

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




@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    if query.get('tag') and kwargs.get('tag'):
        if kwargs.get('tag') not in query.getlist('tag'):
            query.update(kwargs)
        else:
            list_ = query.getlist('tag')
            list_.remove(kwargs.get('tag'))
            query.setlist('tag', list_)
        if query.get('page'):
            query.pop('page')
    else:
        query.update(kwargs)
        if query.get('page'):
            query['page'] = query['page']

    return query.urlencode()
