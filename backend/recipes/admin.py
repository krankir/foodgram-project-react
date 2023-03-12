from django.contrib import admin
from django.contrib.admin import display

from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, \
    IngredientInRecipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites',)
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('count_favorites',)

    @display(description='Количество в избранных.')
    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Favorite)
class Favorite(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
