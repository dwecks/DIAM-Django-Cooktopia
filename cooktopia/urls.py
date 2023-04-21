from django.urls import path
from . import views
from .views import Login, Registration, AddRecipe, AddIngredients, AddSteps

# app_name = 'cooktopia'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes', views.recipes, name='recipes'),
    path('reels', views.reels, name='reels'),
    path('profile', views.profile, name='profile'),
    path("login", Login.as_view(), name="login"),
    path("registration", Registration.as_view(), name="registration"),
    path("addRecipe", AddRecipe.as_view(), name="addRecipe"),
    path("addingredients/<int:recipe_id>/",
         AddIngredients.as_view(), name="addIngredients"),
    path("addsteps/<int:recipe_id>/", AddSteps.as_view(), name="addSteps"),
]
