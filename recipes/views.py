from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.decorators.cache import cache_page
from django.db import transaction

from recipes.forms import RecipeForm, TagRecipeForm
from recipes.models import Recipe, TagRecipe, Ingredient, IngredientsInRecipe


User = get_user_model()


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
        recipes_list = Recipe.objects.filter(
            **{'tags__' + tag: True}).order_by('-pub_date')
    else:
        recipes_list = Recipe.objects.order_by('-pub_date')
    context = get_paginator_context(recipes_list, 9, request)
    return render(request, 'recipes/index.html', context)


def profile(request, author_username, tag=None):
    author = get_object_or_404(User, username=author_username)
    if tag := request.GET.get('tag'):
        if not TagRecipe.validate_tag(tag):
            raise Http404('unknow tag')
        recipes_list = Recipe.objects.filter(**{
            'tags__' + tag: True,
            'author': author,
        }).order_by('-pub_date')
    else:
        recipes_list = Recipe.objects.filter(
            author=author).order_by('-pub_date')
    context = get_paginator_context(recipes_list, 9, request)
    context.setdefault('author', author)
    return render(request, 'recipes/profile.html', context)


@login_required
@transaction.atomic
def add_recipe(request):
    """
    form_tags is dictionary with tag as key and bool as value


    """
    template = 'recipes/recipe_new.html'
    recipe_form = RecipeForm(request.POST or None, files=request.FILES or None)
    #tag_form = TagRecipeForm(request.POST or None) # TODO: clean
    tag_list = TagRecipe.tag_list()

    if request.method == 'POST':
        form_tags = {tag: tag in recipe_form.data for tag in tag_list}
        ingredient_from_form = []

        for k in recipe_form.data:
            if k.split('_')[0] == 'nameIngredient':
                ingr = get_object_or_404(Ingredient, name=recipe_form.data[k])
                amount = recipe_form.data['valueIngredient_' + k.split('_')[1]]
                ingredient_from_form.append(
                    {
                        'ingredient': ingr,
                        'amount': int(amount),
                    }
                )

        if (recipe_form.is_valid() and any(form_tags.values())
                and ingredient_from_form):
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            TagRecipe.objects.create(recipe=recipe, **form_tags)
            for ingr in ingredient_from_form:
                IngredientsInRecipe.objects.create(recipe=recipe, **ingr)

            print('hello')
            return redirect('recipe', recipe.id, recipe.slug)

    context = {'recipe_form': recipe_form, }#'tag_form': tag_form,} # TODO:clean
    return render(request, template, context)


@login_required
@transaction.atomic
def edit_recipe(request, recipe_id=None, the_slug=None):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if not (user.is_staff or user == recipe.author):
        return HttpResponseForbidden

    template = 'recipes/recipe_edit.html'
    recipe_form = RecipeForm(request.POST or None,
                             files=request.FILES or None, instance=recipe)
    # tag_form = TagRecipeForm(request.POST or None)  # TODO: clean
    tag_list = TagRecipe.tag_list()
    ingredients = recipe.ingredients.all()

    if request.method == 'POST':
        form_tags = {tag: tag in recipe_form.data for tag in tag_list}
        ingredient_from_form = []

        for k in recipe_form.data:
            if k.split('_')[0] == 'nameIngredient':
                ingr = get_object_or_404(Ingredient, name=recipe_form.data[k])
                amount = recipe_form.data['valueIngredient_' + k.split('_')[1]]
                ingredient_from_form.append(
                    {
                        'ingredient': ingr,
                        'amount': int(amount),
                    }
                )

        if (recipe_form.is_valid() and any(form_tags.values())
                and ingredient_from_form):
            recipe = recipe_form.save(commit=False)
            recipe.update_slug()
            recipe.save()
            tags = TagRecipe.objects.filter(recipe=recipe)
            tags.update(recipe=recipe, **form_tags)
            for ingr in ingredients:
                ingr.delete()
            for ingr in ingredient_from_form:
                IngredientsInRecipe.objects.create(recipe=recipe, **ingr)

            print('hello')
            return redirect('recipe', recipe.id, recipe.slug)

    context = {'recipe_form': recipe_form, 'recipe': recipe, 'ingredients': ingredients}  # TODO:clean
    return render(request, template, context)


    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post_view', username, post.id)

    context = {'form': form, 'post': post}
    return render(request, 'new_post.html', context)


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
def favorites(request, tag=None):
    user = request.user
    if tag := request.GET.get('tag'):
        if not TagRecipe.validate_tag(tag):
            raise Http404('unknow tag')
        recipes_list = user.favorite_recipes.get_my_recipes().filter(
            **{'tags__' + tag: True}).order_by('-pub_date')
    else:
        recipes_list = user.favorite_recipes.get_my_recipes()
    context = get_paginator_context(recipes_list, 9, request)
    return render(request, 'recipes/index.html', context)


@login_required
def subscriptions(request):
    user = request.user
    authors = user.favorite_authors.get_my_authors()
    context = get_paginator_context(authors, 3, request)
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
