from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import models, transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView

from recipes.forms import RecipeForm
from recipes.models import IngredientsInRecipe, Recipe
from recipes.utils import (
    get_paginator_context, parse_ingredients_from_form,
    print_shoplist, tag_handler_paginator, validate_session_basket)

User = get_user_model()


def index(request):
    query = Recipe.objects.all()
    context = tag_handler_paginator(request, query)
    return render(request, 'recipes/index.html', context)


def profile(request, author_username):
    author = get_object_or_404(User, username=author_username)
    query = Recipe.objects.filter(author=author)
    context = tag_handler_paginator(request, query, {'author': author})
    context.setdefault('author', author)
    return render(request, 'recipes/profile.html', context)


@login_required
def favorites(request):
    user = request.user
    query = user.favorite_recipes.get_my_recipes()
    context = tag_handler_paginator(request, query)
    return render(request, 'recipes/index.html', context)


@login_required
@transaction.atomic
def add_recipe(request):
    """
    tags is dictionary with tag as key and bool as value
    first save recipe for make recipe_id
    then tags and ingredients
    """

    form = RecipeForm(request.POST or None, files=request.FILES or None)
    tag_list = ('breakfast', 'lunch', 'dinner')
    context = {'form': form}

    if request.method == 'POST':
        tags = [tag for tag in tag_list if tag in form.data]
        ingrs_and_amount = parse_ingredients_from_form(form.data)
        if not tags:
            form.add_error(None, 'Нужен хотя бы один тэг')
        if not ingrs_and_amount:
            form.add_error(None, 'Нужен хотя бы один ингредиент. Лучше два.')
        if form.is_valid() and tags and ingrs_and_amount:
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe.tags.add(*tags)
            for ingr in ingrs_and_amount:
                IngredientsInRecipe.objects.create(recipe=recipe, **ingr)

            return redirect('recipe', recipe.id, recipe.slug)

        context['ingredients'] = ingrs_and_amount

    return render(request, 'recipes/recipe_form.html', context)


@login_required
@transaction.atomic
def edit_recipe(request, recipe_id=None, the_slug=None):
    """
    Tags is dictionary with tag as key and bool as value.
    Check permission and then make form from recipe, and
    ingredients from query set to append to form.
    If form contains any data, then for correct update,
    must delete old data.
    When update recipe, then update recipe.slug.
    """
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if not (user.is_staff or user == recipe.author):
        return HttpResponseForbidden

    tag_list = ('breakfast', 'lunch', 'dinner')
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    instance_ingredients = recipe.ingredients.all()

    if request.method == 'POST':
        tags = [tag for tag in tag_list if tag in form.data]
        ingrs_and_amount = parse_ingredients_from_form(form.data)
        if not tags:
            form.add_error(None, 'Нужен хотя бы один тэг')
        if not ingrs_and_amount:
            form.add_error(None, 'Нужен хотя бы один ингредиент. Лучше два.')
        if form.is_valid() and tags and ingrs_and_amount:
            recipe = form.save(commit=False)
            recipe.update_slug()
            recipe.save()
            recipe.tags.clear()
            recipe.tags.add(*tags)
            for ingr in instance_ingredients:
                ingr.delete()
            for ingr in ingrs_and_amount:
                IngredientsInRecipe.objects.create(recipe=recipe, **ingr)

            return redirect('recipe', recipe.id, recipe.slug)

    context = {
        'form': form,
        'recipe': recipe,
        'ingredients': instance_ingredients
    }
    return render(request, 'recipes/recipe_form.html', context)


@login_required
@transaction.atomic
def del_recipe(request, recipe_id=None, the_slug=None):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if user.is_staff or user == recipe.author:
        recipe.delete()
        return redirect('index')
    return HttpResponseForbidden


@login_required
def subscriptions(request):
    user = request.user
    authors = user.favorite_authors.get_my_authors()
    context = get_paginator_context(request, authors, 3)
    return render(request, 'recipes/subscriptions.html', context)


def basket(request):
    if request.user.is_authenticated:
        user = request.user
        recipes_list = user.basket.get_my_recipes()
        context = {'recipes': recipes_list}
        return render(request, 'recipes/basket.html', context)

    basket_for_session = request.session.get('basket')
    recipes_list = []
    if basket_for_session:
        recipes_list = validate_session_basket(request, basket_for_session)

    context = {'recipes': recipes_list}
    return render(request, 'recipes/basket.html', context)


def basket_download(request):
    filename = 'ShopList.txt'
    if request.user.is_authenticated:
        user = request.user
        shoplist = print_shoplist(*user.basket.get_data_for_shoplist(), user)
        response = HttpResponse(shoplist,
                                content_type='text/plain; charset=utf8')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename)
        return response
    basket_for_session = request.session.get('basket')
    if basket_for_session:
        recipes_list = validate_session_basket(request, basket_for_session)
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__in=recipes_list).values(
            'ingredient__name', 'ingredient__unit__name').annotate(
            total=models.Sum('amount'))
        shoplist = print_shoplist(recipes_list, ingredients)
        response = HttpResponse(shoplist,
                                content_type='text/plain; charset=utf8')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename)
        return response
    return HttpResponse('Error request', content_type='text/plain')


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    slug_url_kwarg = 'recipe_id'
    slug_field = 'pk'


def session(request):
    context = {'session': request.session}
    print(request)
    print()
    return render(request, 'recipes/session.html', context)
