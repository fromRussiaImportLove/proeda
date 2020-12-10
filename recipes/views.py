from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView

from recipes.forms import RecipeForm
from recipes.models import IngredientsInRecipe, Recipe, TagRecipe
from recipes.utils import (
    get_paginator_context, parse_ingredients_from_form,
    tag_handler_paginator)

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
    tag_list = TagRecipe.tag_list()

    if request.method == 'POST':
        tags = {tag: tag in form.data for tag in tag_list}
        ingrs_and_amount = parse_ingredients_from_form(form.data)
        if form.is_valid() and any(tags.values()) and ingrs_and_amount:
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            TagRecipe.objects.create(recipe=recipe, **tags)
            for ingr in ingrs_and_amount:
                IngredientsInRecipe.objects.create(recipe=recipe, **ingr)

            return redirect('recipe', recipe.id, recipe.slug)

    context = {'recipe_form': form}
    return render(request, 'recipes/recipe_new.html', context)


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

    tag_list = TagRecipe.tag_list()
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    instance_ingredients = recipe.ingredients.all()

    if request.method == 'POST':
        tags = {tag: tag in form.data for tag in tag_list}
        ingrs_and_amount = parse_ingredients_from_form(form.data)

        if form.is_valid() and any(tags.values()) and ingrs_and_amount:
            recipe = form.save(commit=False)
            recipe.update_slug()
            recipe.save()
            tags_in_instance = TagRecipe.objects.filter(recipe=recipe)
            tags_in_instance.update(recipe=recipe, **tags)
            for ingr in instance_ingredients:
                ingr.delete()
            for ingr in ingrs_and_amount:
                IngredientsInRecipe.objects.create(recipe=recipe, **ingr)

            return redirect('recipe', recipe.id, recipe.slug)

    context = {
        'recipe_form': form,
        'recipe': recipe,
        'ingredients': instance_ingredients
    }
    return render(request, 'recipes/recipe_edit.html', context)


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
