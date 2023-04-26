from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views.generic.edit import UpdateView
from .models import Chef
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import RecipeIngredient
from django.shortcuts import render, redirect
from django.utils import timezone
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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


###############################################################################
# Home Page
###############################################################################

def homeView(request):
    context = {}
    context['top_recipes'] = Recipe.objects.order_by("-rating")[:6]
    context['new_recipes'] = Recipe.objects.order_by('-pub_date')[:6]
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'cooktopia/home.html', context)

###############################################################################
# Recipes
###############################################################################


def recipes(request):
    return render(request, 'cooktopia/recipes.html')


@method_decorator(login_required(login_url='login'), name='dispatch')
class RecipeView(View):
    template_name = "cooktopia/recipe.html"

    def get(self, request, recipe_id):
        context = {}
        context['MEDIA_URL'] = settings.MEDIA_URL
        context["recipe"] = Recipe.objects.get(id=recipe_id)
        return render(request, self.template_name, context)

    def post(self, request, recipe_id):
        pass

def meal_types_view(request):
    meal_types = MealType.objects.all()
    return render(request, 'my_template.html', {'meal_types': meal_types})

def difficulties_view(request):
    difficulties = Difficulty.objects.all()
    return render(request, 'my_template.html', {'difficulties': difficulties})


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
    return render(request, 'filter_by_preparation_time.html', context)
def filter_by_difficulty(request, difficulty_id):
    difficulty = Difficulty.objects.get(pk=difficulty_id)
    recipes = Recipe.objects.filter(difficulty=difficulty)
    return render(request, 'my_template.html', {'recipes': recipes})

def filter_by_meal_type(request, meal_type_id):
    meal_type = MealType.objects.get(pk=meal_type_id)
    recipes = Recipe.objects.filter(meal_type=meal_type)
    return render(request, 'my_template.html', {'recipes': recipes}) #qeq eu ponho aqui

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
    return render(request, 'recipe_list.html', {'recipes': recipes})



# New Recipes Views


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddRecipeView(FormView):
    template_name = "cooktopia/recipeForms/addRecipe.html"
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddIngredientsView(View):
    template_name = "cooktopia/recipeForms/addIngredients.html"

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


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddStepsView(View):
    template_name = "cooktopia/recipeForms/addRecipeSteps.html"

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
        return redirect(reverse("profile", kwargs={"chef_id": self.request.user.chef.id}))

###############################################################################
# Profile Views
###############################################################################


def load_profile_variables(request, chef_id):
    context = {}
    context['chef'] = Chef.objects.get(id=chef_id)
    context["banner"] = context['chef'].recipe_set.order_by("-rating").first()
    context["is_home"] = chef_id == request.user.chef.id
    context["follow_status"] = ChefFollower.objects.filter(
        followed=chef_id, follower=request.user.chef.id).first
    context['MEDIA_URL'] = settings.MEDIA_URL
    return context


@login_required(login_url='login')
def profileView(request, chef_id):
    context = load_profile_variables(request, chef_id)
    context['publications'] = Recipe.objects.filter(chef=chef_id)
    return render(request, 'cooktopia/profile/publications.html', context)


@login_required(login_url='login')
def followersView(request, chef_id):
    context = load_profile_variables(request, chef_id)
    context['followers'] = ChefFollower.objects.filter(followed=chef_id)
    return render(request, 'cooktopia/profile/followers.html', context)


@login_required(login_url='login')
def followingView(request, chef_id):
    context = load_profile_variables(request, chef_id)
    context['following'] = ChefFollower.objects.filter(follower=chef_id)
    return render(request, 'cooktopia/profile/following.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ChefUpdateView(FormView):
    form_class = ChefUpdateForm
    template_name = 'cooktopia/profile/info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chef'] = self.request.user.chef
        context["banner"] = context['chef'].recipe_set.order_by(
            "-rating").first()
        context["is_home"] = True
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        chef = self.request.user.chef

        # fill the form with values from the chef object
        form.fields['name'].initial = chef.name
        form.fields['country'].initial = chef.country
        form.fields['username'].initial = chef.user.username
        form.fields['email'].initial = chef.user.email

        return form

    def form_valid(self, form):
        user = self.request.user
        chef = user.chef

        # Update user fields
        if form.cleaned_data.get('username'):
            user.username = form.cleaned_data['username']
        if form.cleaned_data.get('email'):
            user.email = form.cleaned_data['email']
        if form.cleaned_data.get('password'):
            user.set_password(form.cleaned_data['password'])
        user.save()

        # Update chef fields
        if form.cleaned_data.get('name'):
            chef.name = form.cleaned_data['name']
        if form.cleaned_data.get('country'):
            chef.country = form.cleaned_data['country']
        if form.cleaned_data.get('photo'):
            chef.photo = form.cleaned_data['photo']
        chef.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile", kwargs={"chef_id": self.request.user.chef.id})


@method_decorator(login_required(login_url='login'), name='dispatch')
class addProfileImageView(View):
    def get(self, request):
        form = ProfileImgForm()
        return render(request, "cooktopia/profile/addProfilePhoto.html", {"form": form})

    def post(self, request):
        recived_form = ProfileImgForm(request.POST, request.FILES)
        if recived_form.is_valid():
            chef = request.user.chef
            chef.photo = request.FILES["user_image"]
            chef.save()
            return redirect(reverse("profile", kwargs={"chef_id": self.request.user.chef.id}))
        return render(request, "tempalte path", {"form": recived_form})


@method_decorator(login_required(login_url='login'), name='dispatch')
def toggleFollowView(request, follow_id):
    follower = request.user.chef
    followed = Chef.objects.get(id=follow_id)
    connections = ChefFollower.objects.filter(
        followed=followed.id, follower=follower.id)
    if connections:
        connections.delete()
    else:
        connections = ChefFollower(followed=followed, follower=follower)
        connections.save()
    return redirect(reverse("profile", kwargs={"chef_id": follow_id}))


###############################################################################
# Profile Manage Views
###############################################################################


@login_required(login_url='login')
def manageView(request, chef_id):
    if not request.user.is_staff:
        return redirect(reverse("logout"))

    context = load_profile_variables(request, chef_id)
    return render(request, 'cooktopia/profile/admin.html', context)

###############################################################################
# Login and Registracion Views
###############################################################################


def logoutview(request):
    logout(request)
    return redirect(reverse('home'))


class LoginView(FormView):
    form_class = LoginForm
    template_name = "cooktopia/access/login.html"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

        return self.form_invalid(form)

    def get_success_url(self):
        return reverse("profile", kwargs={"chef_id": self.request.user.chef.id})


class RegistrationView(CreateView):
    model = Chef
    template_name = "cooktopia/access/registration.html"
    form_class = RegitracioForm
    success_url = "login"
