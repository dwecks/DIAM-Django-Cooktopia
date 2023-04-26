from django.urls import path
from . import views
from .views import Login, Registration, AddRecipe, AddIngredients, AddSteps, logoutview, addProfileImage, ChefUpdate

# app_name = 'cooktopia'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes', views.recipes, name='recipes'),
    path('reels', views.reels, name='reels'),
    path('profile/<int:chef_id>/', views.profile, name='profile'),
    path('profile/followers/<int:chef_id>/',
         views.followers, name='followers'),
    path('profile/following/<int:chef_id>/',
         views.following, name='following'),
    path('profile/Info/<int:chef_id>/', ChefUpdate.as_view(), name='profileInfo'),
    path('profile/addphoto', addProfileImage.as_view(), name='profileImg'),
    path("login", Login.as_view(), name="login"),
    path('logout/', logoutview, name='logout'),
    path("registration", Registration.as_view(), name="registration"),
    path("addRecipe", AddRecipe.as_view(), name="addRecipe"),
    path("addingredients/<int:recipe_id>/",
         AddIngredients.as_view(), name="addIngredients"),
    path("addsteps/<int:recipe_id>/", AddSteps.as_view(), name="addSteps"),
]
