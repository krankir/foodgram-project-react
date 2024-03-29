from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import IngredientViewSet, TagViewSet, RecipeViewSet

app_name = 'api'

router = DefaultRouter()

router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),
]
