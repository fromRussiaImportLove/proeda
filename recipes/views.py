from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from recipes.models import Recipe

def get_paginator_context(posts_list, page_slice, request) -> dict:
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return context


def page_not_found(request, exception):
    return render(request, "misc/404.html",
                  {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


# @cache_page(20 * 60)
def index(request):
    posts_list = Recipe.objects.all()
    context = get_paginator_context(posts_list, 10, request)
    return render(request, 'recipes/index.html', context)
