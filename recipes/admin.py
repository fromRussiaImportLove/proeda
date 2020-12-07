from django.contrib import admin

from recipes.models import (
    Basket, Favorite, Follow, Ingredient, IngredientsInRecipe, Recipe,
    TagRecipe, Unit)

admin.site.empty_value_display = '-пусто-'


class TagInline(admin.StackedInline):
    model = TagRecipe
    can_delete = False


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author',
                   'tags__breakfast', 'tags__lunch', 'tags__dinner')
    date_hierarchy = 'pub_date'
    readonly_fields = ('followers_count',)

    inlines = [
        TagInline,
    ]

    def followers_count(self, instance):
        return instance.followers.count()


@admin.register(Unit, Ingredient)
class SimpeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    search_fields = ('recipe',)
    list_filter = ('breakfast', 'lunch', 'dinner')
    list_display = ('recipe', 'breakfast', 'lunch', 'dinner')


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
