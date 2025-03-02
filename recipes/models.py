from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import PositiveSmallIntegerField
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import Adjust, ResizeToFill
from pytils.translit import slugify

from taggit.managers import TaggableManager, _TaggableManager


User = get_user_model()


class NonZeroPositiveSmallIntegerField(PositiveSmallIntegerField):
    description = "Non zero positive small integer"

    def get_internal_type(self):
        return "PositiveSmallIntegerField"

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 1,
            **kwargs,
        })


class Unit(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}, {self.unit}'


class _CustomTaggableManager(_TaggableManager):
    @property
    def breakfast(self):
        return self.instance.tags.filter(name='breakfast').exists()

    @property
    def lunch(self):
        return self.instance.tags.filter(name='lunch').exists()

    @property
    def dinner(self):
        return self.instance.tags.filter(name='dinner').exists()


class RecipeManager(models.Manager):
    def get_three_last(self):
        return self.order_by('-pub_date')[:3]


class Recipe(models.Model):
    name = models.CharField(verbose_name='Название рецепта', max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Картинка', upload_to='recipes/')
    image_max_size = ImageSpecField(
        [Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(480, 480)],
        source='image',
        format='JPEG',
        options={'quality': 90}
    )
    image_med_size = ImageSpecField(
        [Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(363, 363)],
        source='image',
        format='JPEG',
        options={'quality': 90}
    )
    image_small_size = ImageSpecField(
        [Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(90, 90)],
        source='image',
        format='JPEG',
        options={'quality': 90}
    )
    cooking_time = NonZeroPositiveSmallIntegerField(
        verbose_name='Время готовки', )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    slug = models.SlugField(
        verbose_name='SLUG-ссылка',
        null=True,
        blank=True,
        unique=True,
    )

    objects = RecipeManager()
    tags = TaggableManager(manager=_CustomTaggableManager)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipe', args=(self.id, self.slug))

    def update_slug(self):
        self.slug = slugify(f'{self.name}')


class IngredientsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='recipes',
    )
    amount = NonZeroPositiveSmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount} {self.ingredient.unit}'


class FollowManager(models.Manager):
    def is_follow(self, author, user):
        if user.is_authenticated:
            return super().filter(author=author, user=user).exists()
        return False

    def recipes(self):
        """
        :return: Возвращает список всех рецептов всех авторов,
        на которых подписан пользователь,
        отсортированный от новых к старым
        """
        authors = self.all().values('author_id')
        recipes_list = Recipe.objects.filter(
            author__in=authors).order_by('-pub_date')
        return recipes_list

    def get_my_authors(self):
        """:return: Возвращает список любимых авторов"""
        authors = self.all().values('author_id')
        queryset = User.objects.filter(id__in=authors)
        return queryset

    def check_related_name(self, user_obj):
        """
        Расставляем автора и пользователя в зависимости от realted_name
        Дополнительная функция, которая в зависимости от отношений
        (соответствующего сета) понимает кто есть автор, а кто пользователь
        сделана для универсальности вызова функций contains, append, remove
        """
        user, author = self.instance, user_obj
        if self.field.name == 'author':
            user, author = author, user
        return user, author

    def contains(self, user_obj):
        """
        Универсальный метод для проверки followers и following

        Одинаково корректно проверят вне зависимости от related_name.
        Можно использовать как user.follower.contains(author)
        Чтобы проверить есть ли автор в подписках пользователя
        И можно наоборот author.following.contains(user)
        Чтобы проверить есть ли пользователь в последователях у автора.

        :param user_obj: в зависимости от контекста user или author
        """
        user, author = self.check_related_name(user_obj)
        return self.is_follow(author=author, user=user)

    def append(self, user_obj):
        """
        Универасальный метод добавить как любимого автора так и подписчика
        Вызывается подобно contains:
        user.follower.append(author)
        author.following.append(user)
        """
        user, author = self.check_related_name(user_obj)
        if author != user:
            self.get_or_create(user=user, author=author)

    def remove(self, user_obj):
        """ Универсальный метод по удалению любимого автора или подписчика """
        user, author = self.check_related_name(user_obj)
        follow = self.filter(user=user, author=author)
        follow.delete()

    def switch(self, user_obj):
        """ Метод который позволят переключать состояние: подписан/нет """
        if self.contains(user_obj):
            self.remove(user_obj)
        else:
            self.append(user_obj)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_authors',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )

    objects = FollowManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_follow')]

    def __str__(self):
        return f'{self.user.username} follow to {self.author.username}'


class FavoriteManager(models.Manager):
    def is_follow(self, recipe, user):
        if user.is_authenticated:
            return super().filter(recipe=recipe, user=user).exists()
        return False

    def get_my_recipes(self):
        """
        :return: Возвращает список рецептов пользователя,
        добавленные в избранное
        """
        recipes = self.instance.favorite_recipes.values('recipe_id')
        queryset = Recipe.objects.filter(id__in=recipes).order_by('-pub_date')
        return queryset

    def append(self, recipe):
        """
        Метод добавления рецепта в избранное
        Вызывается user.favorite_recipes.append(recipe)
        """
        user = self.instance
        if user.is_authenticated:
            self.get_or_create(user=user, recipe=recipe)

    def remove(self, recipe):
        """
        Удаляем из избранного.
        Вызывается user.favorite_recipes.remove(recipe)
        """
        user = self.instance
        if user.is_authenticated:
            favorite = self.filter(user=user, recipe=recipe)
            favorite.delete()

    def switch(self, recipe):
        """ Метод который позволят переключать состояние: добавлен/нет """
        if self.is_follow(recipe, self.instance):
            self.remove(recipe)
        else:
            self.append(recipe)


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='followers',
    )

    objects = FavoriteManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_favorite')]

    def __str__(self):
        return f'{self.user.username} like {self.recipe.name}'


class BasketManager(models.Manager):
    def is_in_basket(self, recipe, user):
        if user.is_authenticated:
            return super().filter(recipe=recipe, user=user).exists()
        return False

    def get_my_recipes(self):
        """
        :return: Возвращает список рецептов пользователя,
        добавленных в корзину
        """
        recipes = [r.recipe.id for r in self.instance.basket.all()]
        queryset = Recipe.objects.filter(id__in=recipes).order_by('name')
        return queryset

    def append(self, recipe):
        """
        Метод добавления рецепта в корзину
        Вызывается user.basket.append(recipe)
        """
        user = self.instance
        self.get_or_create(user=user, recipe=recipe)

    def remove(self, recipe):
        """
        Удаляем из корзины.
        Вызывается user.basket.remove(recipe)
        """
        user = self.instance
        basked_item = self.filter(user=user, recipe=recipe)
        basked_item.delete()

    def clear(self, recipe):
        """ Метод который удаляет все из корзины пользователя """
        user = self.instance
        basked_items = self.filter(user=user)
        basked_items.delete()

    def get_data_for_shoplist(self):
        """ Метод возвращает два querysetа из ингридиентов и блюд"""
        basked_items = self.get_my_recipes()
        basked_recipes = self.all().values('recipe_id')
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__in=basked_recipes).values(
            'ingredient__name', 'ingredient__unit__name').annotate(
            total=models.Sum('amount'))

        return basked_items, ingredients


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='buyers',
    )

    objects = BasketManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_basket')]

    def __str__(self):
        return f'{self.user.username} want {self.recipe.name}'
