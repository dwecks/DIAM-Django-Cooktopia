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
from django.db.models import Q
from .models import Recipe

# forms
from django.views.generic.edit import CreateView, FormView
from .forms import *

# settings
from django.conf import settings

# Create your views here.


def home(request):
    context = {}
    context['top_recipes'] = Recipe.objects.order_by("-rating")[:3]
    context['new_recipes'] = Recipe.objects.order_by('-pub_date')[:4]
    print(
        f"************************************************ {context['top_recipes']}")
    print(
        f"************************************************ {context['new_recipes']}")
    return render(request, 'cooktopia/home.html', context)

def recipes(request):
    context = {}
    context['top_recipes'] = Recipe.objects.order_by("-rating")[:3]
    context['new_recipes'] = Recipe.objects.order_by('-pub_date')[:4]
    print(
        f"************************************************ {context['top_recipes']}")
    print(
        f"************************************************ {context['new_recipes']}")
    return render(request, 'cooktopia/recipes.html', context)




def reels(request):
    return render(request, 'cooktopia/reels.html')

def meal_types_view(request):
    meal_types = MealType.objects.all()
    print(meal_types)
    return render(request, 'recipes.html', {'meal_types': meal_types})



def difficulties_view(request):
    difficulties = Difficulty.objects.all()
    return render(request, 'recipes.html', {'difficulties': difficulties})


def filter_by_preparation_time(request):
    # Retrieve the selected preparation time ranges from the request
    time_ranges = request.GET.getlist('preparationTime')

    # Create a list of Q objects to filter the recipes
    filters = []
    for time_range in time_ranges:
        if time_range == '0,30':
            filters.append(Q(preparationTime__lte=30))
        elif time_range == '30,60':
            filters.append(Q(preparationTime__gt=30) & Q(preparationTime__lte=60))
        elif time_range == '60,':
            filters.append(Q(preparationTime__gt=60))

    # Apply the filters to the Recipe model
    if filters:
        recipes = Recipe.objects.filter(*filters)
    else:
        recipes = Recipe.objects.all()

    # Pass the filtered recipes to the template
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes.html', context)
def filter_by_difficulty(request, difficulty_id):
    difficulty = Difficulty.objects.get(pk=difficulty_id)
    recipes = Recipe.objects.filter(difficulty=difficulty)
    return render(request, 'recipes.html', {'recipes': recipes})

def filter_by_meal_type(request, meal_type_id):
    meal_type = MealType.objects.get(pk=meal_type_id)
    recipes = Recipe.objects.filter(meal_type=meal_type)
    return render(request, 'recipes.html', {'recipes': recipes}) #qeq eu ponho aqui

def filter_by_bub_date(request):
    today = timezone.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    last_year = today - timedelta(days=365)
    pub_date = request.GET.get('pub_date')
    if pub_date == 'week':
        recipes = Recipe.objects.filter(published_date__gte=last_week)
    elif pub_date == 'month':
        recipes = Recipe.objects.filter(published_date__gte=last_month)
    elif pub_date == 'year':
        recipes = Recipe.objects.filter(published_date__gte=last_year)
    else:
        recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})



@login_required(login_url='login')
def profile(request):
    context = {'MEDIA_URL': settings.MEDIA_URL, "range": range(1, 10)}
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
        recipe.image = self.request.FILES['image']
        recipe.save()
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
