from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель списка тегов."""
    name = models.CharField('Название тега', max_length=100, unique=True,)
    color = models.CharField('Цвет', max_length=7, unique=True,)
    slug = models.SlugField('Уникальный слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField('Название ингредиента', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=50)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField('Название рецепта', max_length=250)
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE, related_name='recipes',
                               )
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         through='IngredientInRecipe',
                                         verbose_name='Ингридиенты',
                                         )
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Теги',
                                  )
    image = models.ImageField('Изображение', blank=True, null=True,
                              upload_to='image_recipes/',
                              )
    text = models.TextField('Описание',)
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1,
                                      message='Минимальное значение 1Минута!')]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class IngredientInRecipe(models.Model):
    """Промежуточная модель ингредиента и его количества в рецепте."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients_amount',
                               verbose_name='Рецепт',
                               )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        default=1,
        validators=[MinValueValidator(1, message='Минимальное количество 1!')]
    )

    class Meta:
        verbose_name = 'Ингридиент для рецепта'
        verbose_name_plural = 'Ингридиенты для рецепта'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}'


class Favorite(models.Model):
    """Модель избранного рецепта."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь',
                             )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites',
                               verbose_name='Рецепт',
                               )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe.name}'


class ShoppingCart(models.Model):
    """Модель корзины покупок."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='cart',
                             verbose_name='Пользователь',
                             )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='cart',
                               verbose_name='Рецепт',
                               )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_user'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
