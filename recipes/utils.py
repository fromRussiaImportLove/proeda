from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, TagRecipe


def get_paginator_context(request, objects_list, page_slice=9) -> dict:
    paginator = Paginator(objects_list, page_slice)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return context


def tag_handler(request, queryset_without_tag, filter_kwargs=None):
    if tag := request.GET.get('tag'):
        if not TagRecipe.validate_tag(tag):
            raise Http404('unknow tag')
        if filter_kwargs is None:
            queryset_with_tag = queryset_without_tag.filter(
                **{'tags__' + tag: True})
        else:
            queryset_with_tag = queryset_without_tag.filter(
                **{'tags__' + tag: True}, **filter_kwargs)
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
