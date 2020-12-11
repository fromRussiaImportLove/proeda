from django.contrib import admin

from recipes.models import (
    Basket, Favorite, Follow, Ingredient, IngredientsInRecipe, Recipe, Unit)

admin.site.empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author',
                   'tags')
    date_hierarchy = 'pub_date'
    readonly_fields = ('followers_count',)

    def followers_count(self, instance):
        return instance.followers.count()


@admin.register(Unit, Ingredient)
class SimpeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display_links = ('recipe', 'ingredient')
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    autocomplete_fields = ('ingredient',)


@admin.register(Follow, Favorite, Basket)
class SimpeStrAdmin(admin.ModelAdmin):
    list_display_links = ('__str__',)
    list_display = ('pk', '__str__')
    list_filter = ('user',)
