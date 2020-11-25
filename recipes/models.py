from django.db import models
from django.conf import settings

from pytils.translit import slugify

User = settings.AUTH_USER_MODEL


class Tag(models.TextChoices):
    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'


class Unit(models.Model):
    name = models.CharField(max_length=16)


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    units = models.ForeignKey(Unit, on_delete=models.PROTECT)


class Recipe(models.Model):
    name = models.CharField(verbose_name='Название рецепта', max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='recipes/', null=True, blank=True)
    tag = models.CharField(max_length=128, choices=Tag.choices)
    cooking_time = models.IntegerField(verbose_name='Время готовки')
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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.pk}-{self.name}')
        return super().save(*args, **kwargs)


class IngredientsInRecipes(models.Model):
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
    amount = models.IntegerField(verbose_name='Количество')


class FollowManager(models.Manager):
    def is_follow(self, author, user):
        if user.is_authenticated:
            return super().filter(author=author, user=user).exists()
        return False

    def recipes(self):
        """
        :return: Возвращает список рецептов пользователя,
        отсортированный от новых к старым
        """
        authors = self.all().values('author_id')
        recipes_list = Recipe.objects.filter(
            author__in=authors).order_by('-pub_date')
        return recipes_list

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
        models.UniqueConstraint(fields=['user', 'author'],
                                name='unique_follow')

    def __str__(self):
        return f'{self.user.username} follow to {self.author.username}'


class FavoriteManager(models.Manager):
    def is_follow(self, recipe, user):
        if user.is_authenticated:
            return super().filter(recipe=recipe, user=user).exists()
        return False

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
        models.UniqueConstraint(fields=['user', 'recipe'],
                                name='unique_follow')

    def __str__(self):
        return f'{self.user.username} like {self.recipe.name}'


class BasketManager(models.Manager):
    def is_basked(self, recipe, user):
        if user.is_authenticated:
            return super().filter(recipe=recipe, user=user).exists()
        return False

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

    def shoplist(self):
        """ Метод возвращает queryset из ингридиентов и количества"""
        # basked_items = self.filter(user=self.instance)
        basked_recipes = self.all().values('recipe_id')
        ingredients = IngredientsInRecipes.objects.filter(
            recipe__in=basked_recipes).annotate(amount=models.Sum('amount'))
        return ingredients


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
        models.UniqueConstraint(fields=['user', 'recipe'],
                                name='unique_follow')

    def __str__(self):
        return f'{self.user.username} want {self.recipe.name}'
