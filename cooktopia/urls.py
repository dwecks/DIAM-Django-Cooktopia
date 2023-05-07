from django.urls import path
from . import views
from .views import LoginView, RegistrationView, AddRecipeView, AddIngredientsView, AddStepsView, logoutview, addProfileImageView, ChefUpdateView, RecipeView, UserQuestionView

# app_name = 'cooktopia'


urlpatterns = [
    # Core
    path('', views.homeView, name='home'),
    # Recipes
    path('recipes', views.recipes, name='recipes'),
    path('recipes/<int:recipe_id>/', RecipeView.as_view(), name='recipe'),
    path('recipes/filter', views.filter_recipes, name='filter_recipes'),
    # new Recipes
    path("createrecipe", AddRecipeView.as_view(), name="addRecipe"),
    path("createrecipe/ingredients/<int:recipe_id>/",
         AddIngredientsView.as_view(), name="addIngredients"),
    path("createrecipe/steps/<int:recipe_id>/",
         AddStepsView.as_view(), name="addSteps"),
    # Profile
    path('profile/<int:chef_id>/', views.profileView, name='profile'),
    path('profile/followers/<int:chef_id>/',
         views.followersView, name='followers'),
    path('profile/following/<int:chef_id>/',
         views.followingView, name='following'),
    path('profile/Info/<int:chef_id>/',
         ChefUpdateView.as_view(), name='profileInfo'),
    path('profile/addphoto', addProfileImageView.as_view(), name='profileImg'),
    path('profile/follow/<int:follow_id>',
         views.toggleFollowView, name='follow'),
    path('profile/admin/<int:chef_id>/', views.manageView, name='manage'),

    # Access and Registracion
    path("login", LoginView.as_view(), name="login"),
    path('logout/', logoutview, name='logout'),
    path("registration", RegistrationView.as_view(), name="registration"),
    # User Help
    path("help", UserQuestionView.as_view(), name="help"),
    # React
    path('api/recipes/', views.list_recipes),
    path('api/recipes/<int:id>', views.edit_recipe),
    path('api/chefs/', views.list_chef),
    path('api/chefs/<int:id>', views.edit_chef),
]
