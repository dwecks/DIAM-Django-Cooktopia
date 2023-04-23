from .models import RecipeIngredient
from django.shortcuts import render, redirect
from django.utils import timezone
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views import View
from .models import MealType

# forms
from django.views.generic.edit import CreateView, FormView
from .forms import *

# settings
from django.conf import settings

# Create your views here.


def home(request):
    return render(request, 'cooktopia/home.html')


def recipes(request):
    return render(request, 'cooktopia/recipes.html')


def reels(request):
    return render(request, 'cooktopia/reels.html')

def my_view(request):
    meal_types = MealType.objects.all()
    return render(request, 'my_template.html', {'meal_types': meal_types})

def my_view(request):
    difficulties = Difficulty.objects.all()
    return render(request, 'my_template.html', {'difficulties': difficulties})


@login_required(login_url='login')
def profile(request):
    context = {'MEDIA_URL': settings.MEDIA_URL, }
    print(settings.MEDIA_URL)
    print(settings.MEDIA_ROOT)
    return render(request, 'cooktopia/profile.html', context)


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


class AddRecipe(FormView):
    template_name = "cooktopia/addRecipe.html"
    form_class = AddRecipeForm

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.chef = self.request.user.chef
        recipe.pub_date = timezone.now()
        recipe.rating = 0
        recipe.save()
        recipe.id = 2
        return HttpResponseRedirect(reverse('addIngredients', args=[recipe.id]))
        # return super().form_valid(form)


class AddIngredients(View):
    template_name = "cooktopia/addIngredients.html"

    def get(self, request, recipe_id):
        formset = RecipeIngredientFormSet(
            queryset=RecipeIngredient.objects.none())
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, recipe_id):
        formset = RecipeIngredientFormSet(request.POST)
        recipe = Recipe.objects.get(id=recipe_id)
        for form in formset:
            if form.is_valid() and form.cleaned_data.get('ingredient') and form.cleaned_data.get('quantity'):
                recipe_ingredient = form.save(commit=False)
                recipe_ingredient.recipe = recipe
                recipe_ingredient.ingredient = form.cleaned_data['ingredient']
                recipe_ingredient.save()
        return redirect(reverse('addSteps', kwargs={'recipe_id': recipe_id}))


class AddSteps(View):
    template_name = "cooktopia/addRecipeSteps.html"

    def get(self, request, recipe_id):
        formset = RecipeStepsFormSet(
            queryset=RecipeSteps.objects.none())
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, recipe_id):
        formset = RecipeStepsFormSet(request.POST)
        recipe = Recipe.objects.get(id=recipe_id)
        for form in formset:
            if form.is_valid() and form.cleaned_data.get('step'):
                recipe_step = form.save(commit=False)
                recipe_step.recipe = recipe
                recipe_step.save()
        return redirect(reverse('profile'))
