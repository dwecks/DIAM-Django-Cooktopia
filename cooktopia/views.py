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

# forms
from django.views.generic.edit import CreateView, FormView
from .forms import *

# settings
from django.conf import settings

# Create your views here.


def home(request):
    context = {}
    context['top_recipes'] = Recipe.objects.order_by("-rating")[:6]
    context['new_recipes'] = Recipe.objects.order_by('-pub_date')[:6]
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'cooktopia/home.html', context)


def recipes(request):
    return render(request, 'cooktopia/recipes.html')


def reels(request):
    context = {}
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'cooktopia/reels.html', context)


@login_required(login_url='login')
def profile(request, chef_id):
    context = {}
    context['chef'] = Chef.objects.get(id=chef_id)
    context['publications'] = Recipe.objects.filter(chef=chef_id)
    context['top_recipes'] = Recipe.objects.order_by("-rating")[:6]
    context["banner"] = context['chef'].recipe_set.order_by("-rating").first()
    context["is_home"] = chef_id == request.user.chef.id
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'cooktopia/publications.html', context)


@login_required(login_url='login')
def followers(request, chef_id):
    context = {}
    context['chef'] = Chef.objects.get(id=chef_id)
    context['followers'] = ChefFollower.objects.filter(followed=chef_id)
    context["banner"] = context['chef'].recipe_set.order_by("-rating").first()
    context["is_home"] = chef_id == request.user.chef.id
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'cooktopia/followers.html', context)


@login_required(login_url='login')
def following(request, chef_id):
    context = {}
    context['chef'] = Chef.objects.get(id=chef_id)
    context['following'] = ChefFollower.objects.filter(follower=chef_id)
    context["banner"] = context['chef'].recipe_set.order_by("-rating").first()
    context["is_home"] = chef_id == request.user.chef.id
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'cooktopia/following.html', context)


class addProfileImage(View):
    def get(self, request):
        form = ProfileImgForm()
        return render(request, "cooktopia/addProfilePhoto.html", {"form": form})

    def post(self, request):
        recived_form = ProfileImgForm(request.POST, request.FILES)
        if recived_form.is_valid():
            chef = request.user.chef
            chef.photo = request.FILES["user_image"]
            chef.save()
            return redirect(reverse("profile", kwargs={"chef_id": self.request.user.chef.id}))
        return render(request, "tempalte path", {"form": recived_form})


def logoutview(request):
    logout(request)
    return redirect(reverse('home'))


class Login(FormView):
    form_class = LoginForm
    template_name = "cooktopia/login.html"

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


class Registration(CreateView):
    model = Chef
    template_name = "cooktopia/registration.html"
    form_class = RegitracioForm
    success_url = "login"


class ChefUpdate(FormView):
    form_class = ChefUpdateForm
    template_name = 'cooktopia/info.html'

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
        if form.cleaned_data.get('photo'):
            chef.photo = form.cleaned_data['photo']
        chef.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile", kwargs={"chef_id": self.request.user.chef.id})


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
        return redirect(reverse("profile", kwargs={"chef_id": self.request.user.chef.id}))
