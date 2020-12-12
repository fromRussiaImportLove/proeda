from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from taggit.models import Tag

from recipes.models import Ingredient


def get_paginator_context(request, objects_list, page_slice=9) -> dict:
    paginator = Paginator(objects_list, page_slice)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return context


def tag_handler(request, queryset_without_tag, filter_kwargs=None):
    if tag := request.GET.get('tag'):
        tag = get_object_or_404(Tag, name=tag)
        if filter_kwargs is None:
            queryset_with_tag = queryset_without_tag.filter(
                tags__name=tag)
        else:
            queryset_with_tag = queryset_without_tag.filter(
                tags__name=tag, **filter_kwargs)
        return queryset_with_tag
    else:
        return queryset_without_tag


def tag_handler_paginator(request, queryset_without_tag, filter_kwargs=None):
    taged_queryset = tag_handler(request, queryset_without_tag, filter_kwargs)
    return get_paginator_context(request, taged_queryset)


def parse_ingredients_from_form(form_data):
    ingredient_from_form = []
    for k in form_data:
        if k.split('_')[0] == 'nameIngredient':
            ingr = get_object_or_404(Ingredient, name=form_data[k])
            amount = form_data['valueIngredient_' + k.split('_')[1]]
            ingredient_from_form.append(
                {
                    'ingredient': ingr,
                    'amount': int(amount),
                }
            )
    return ingredient_from_form


def print_shoplist(basked_items, ingredients):
    shoplist = (f"{'Ваш список покупок от сервиса про`Еда':^80}"
                '\n\nДля приготовления выбранных вами блюд:\n')
    for num, item in enumerate(basked_items, 1):
        shoplist += f'\t {str(num)}. {item}\n'
    shoplist += '\nВам понадобятся следующие продукты:\n'
    for num, item in enumerate(ingredients, 1):
        shoplist += (f'\t{str(num)}. '
                     f'{item["ingredient__name"]:<57}: {str(item["total"]):<4}'
                     f'{item["ingredient__unit__name"]:<10} \t[  ]\n')
    shoplist += '\n\tПриятного аппетита!\n\thttp://proeda.lukojo.com'

    return shoplist
