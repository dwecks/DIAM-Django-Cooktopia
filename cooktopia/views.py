from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
# forms
from django.views.generic.edit import CreateView, FormView
from .forms import *


# Create your views here.


def home(request):
    return render(request, 'cooktopia/home.html')


def recipes(request):
    return render(request, 'cooktopia/recipes.html')


def reels(request):
    return render(request, 'cooktopia/reels.html')


@login_required(login_url='login')
def profile(request):
    return render(request, 'cooktopia/profile.html')


class Login(FormView):
    form_class = LoginForm
    template_name = "cooktopia/login.html"
    success_url = "profile"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

        return self.form_invalid(form)


class Registration(CreateView):
    model = Chef
    template_name = "cooktopia/registration.html"
    form_class = RegitracioForm
    success_url = "profile"
