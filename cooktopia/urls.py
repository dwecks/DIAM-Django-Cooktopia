from django.urls import path
from . import views
from .views import Login, Registration

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes', views.recipes, name='recipes'),
    path('reels', views.reels, name='reels'),
    path('profile', views.profile, name='profile'),
    path("login", Login.as_view(), name="login"),
    path("registration", Registration.as_view(), name="registration"),
]
