from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.decorators.cache import cache_page

from recipes.models import Recipe, TagRecipe


def get_paginator_context(objects_list, page_slice, request) -> dict:
    paginator = Paginator(objects_list, page_slice)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return context


# @cache_page(20 * 60)
def index(request, tag=None):
    if tag := request.GET.get('tag'):
        if not TagRecipe.validate_tag(tag):
            raise Http404('unknow tag')
        recipes_list = Recipe.objects.filter(**{'tags__' + tag: True})
    else:
        recipes_list = Recipe.objects.all()
    context = get_paginator_context(recipes_list, 9, request)
    return render(request, 'recipes/index.html', context)


@login_required
def favorites(request, tag=None):
    user = request.user
    if tag := request.GET.get('tag'):
        if not TagRecipe.validate_tag(tag):
            raise Http404('unknow tag')
        recipes_list = user.favorite_recipes.get_my_recipes().filter(
            **{'tags__' + tag: True})
    else:
        recipes_list = user.favorite_recipes.get_my_recipes()
    context = get_paginator_context(recipes_list, 9, request)
    return render(request, 'recipes/index.html', context)


@login_required
def basket(request):
    user = request.user
    recipes_list = user.basket.get_my_recipes()
    return render(request, 'recipes/basket.html', {'recipes': recipes_list})

@login_required()
def basket_download(request):
    user = request.user
    shoplist = user.basket.shoplist()
    return HttpResponse(shoplist, content_type='text/plain; charset=utf8')


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    slug_url_kwarg = 'recipe_id'
    slug_field = 'pk'
