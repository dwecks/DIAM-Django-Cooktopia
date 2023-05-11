
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .serializers import *
from django.views.generic.edit import CreateView, FormView
from .forms import *
from django.conf import settings
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from .models import Recipe
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Q

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

# All recipes


def recipes(request):
    context = {}
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['meal_types'] = MealType.objects.all()
    context["difficulties"] = Difficulty.objects.all()
    return render(request, 'cooktopia/recipes.html', context)

# 1 Recipe Pgae


@method_decorator(login_required(login_url='login'), name='dispatch')
class RecipeView(View):
    template_name = "cooktopia/recipe.html"

    def get(self, request, recipe_id):
        context = {}
        context['MEDIA_URL'] = settings.MEDIA_URL
        context["recipe"] = get_object_or_404(Recipe, id=recipe_id)
        context["steps"] = RecipeSteps.objects.filter(recipe=context["recipe"])
        context["comments"] = Comment.objects.filter(recipe=context["recipe"])
        context["ingredients"] = RecipeIngredient.objects.filter(
            recipe=context["recipe"])
        context['related_recipes'] = Recipe.objects.filter(
            mealType=context["recipe"].mealType)[:3]
        context["commentForm"] = CommentForm()
        context["ratingForm"] = RatingForm()
        context["recipe"] = Recipe.objects.get(id=recipe_id)
        return render(request, self.template_name, context)

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        comment_form = CommentForm(
            request.POST, request=request, recipe=recipe)
        rating_form = RatingForm(request.POST, recipe=recipe)

        if comment_form.is_valid():
            comment_form.save()

        if rating_form.is_valid():
            rating_form.save()

        return HttpResponseRedirect(reverse('recipe', args=[recipe_id]))


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
    context['chef'] = get_object_or_404(Chef, id=chef_id)
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


@login_required(login_url='login')
def toggleFollowView(request, follow_id):
    follower = request.user.chef
    followed = get_object_or_404(Chef, id=follow_id)
    connections = ChefFollower.objects.filter(
        followed=followed.id, follower=follower.id)
    if connections:
        connections.delete()
    else:
        connections = ChefFollower(followed=followed, follower=follower)
        connections.save()
    return redirect(reverse("profile", kwargs={"chef_id": follow_id}))


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


def terms_of_service(request):
    context = {}
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'cooktopia/termsOfService.html', context)

###############################################################################
# Help views
###############################################################################


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserQuestionView(CreateView):
    model = UserHelp
    template_name = "cooktopia/help/userquestion.html"
    form_class = HelpForm
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


# Profile Manage Views
@login_required(login_url='login')
def manageView(request, chef_id):
    if not request.user.is_staff:
        return redirect(reverse("logout"))

    context = load_profile_variables(request, chef_id)
    context["user_questions"] = UserHelp.objects.all()
    return render(request, 'cooktopia/profile/admin.html', context)

###############################################################################
# React Views
###############################################################################


@api_view(['GET', 'POST'])
def list_recipes(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serialized_recipes = RecipeSerializer(
            recipes, context={'request': request}, many=True)
        return Response(serialized_recipes.data)
    elif request.method == 'POST':
        serializer_recipe = RecipeSerializer(data=request.data)
        if serializer_recipe.is_valid():
            serializer_recipe.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer_recipe.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def edit_recipe(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer_recipe = RecipeSerializer(
            recipe, data=request.data, context={'request': request})
        if serializer_recipe.is_valid():
            serializer_recipe.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer_recipe.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def list_chef(request):
    if request.method == 'GET':
        chefs = Chef.objects.all()
        serialized_chefs = ChefSerializer(
            chefs, context={'request': request}, many=True)
        return Response(serialized_chefs.data)
    elif request.method == 'POST':
        serializer_chef = ChefSerializer(data=request.data)
        if serializer_chef.is_valid():
            serializer_chef.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer_chef.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def edit_chef(request, id):
    try:
        chef = Chef.objects.get(id=id)
    except Chef.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer_chef = ChefSerializer(
            chef, data=request.data, context={'request': request})
        if serializer_chef.is_valid():
            serializer_chef.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer_chef.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        chef.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
