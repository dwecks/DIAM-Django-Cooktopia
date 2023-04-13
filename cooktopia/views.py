from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'cooktopia/home.html')


def recipes(request):
    return render(request, 'cooktopia/recipes.html')


def reels(request):
    return render(request, 'cooktopia/reels.html')


def profile(request):
    return render(request, 'cooktopia/profile.html')
