from django.core.exceptions import ValidationError
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'lbl-r l2-r', 'placeholder': 'Username'}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'lbl-r l2-r', 'placeholder': 'Password'}))


class RegitracioForm(forms.ModelForm):
    nome = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'lbl-r l2-r', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'lbl-r l2-r', 'placeholder': 'example@exemple.com'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'lbl-r l2-r', 'placeholder': 'Password'}))

    class Meta:
        model = Chef
        fields = ["name"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'lbl-r l2-r', 'placeholder': 'Name'}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['nome'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        chef = super().save(commit=False)  # Retorno o elemento
        chef.user = user                  # para podermos adicionar o atributo user
        if commit:
            chef.save()
        return chef


class AddRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ["title", "description",
                  "preparationTime", "mealType", "difficulty"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'lbl-r l2-r', 'placeholder': "What's the title of this culinary creation?"},),
            'description': forms.Textarea(attrs={'class': 'lbl-r l2-r', 'placeholder': "Describe this dish to someone who's never tasted it before?"},),
            'preparationTime': forms.TextInput(attrs={'class': 'lbl-r l2-r', 'placeholder': 'How many minutes until this masterpiece is ready?'},),
            'mealType': forms.Select(attrs={'class': 'lbl-r l2-r'}),
            'difficulty': forms.Select(attrs={'class': 'lbl-r l2-r'})
        }


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'ingredient']
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'lbl-r l2-r q-ingredient', 'placeholder': 'Quantity?'},),
            'ingredient': forms.Select(attrs={'class': 'lbl-r l2-r ingredient'})
        }
        required = {
            'ingredient': False,
            'quantity': False,
        }


RecipeIngredientFormSet = modelformset_factory(
    RecipeIngredient, form=RecipeIngredientForm, extra=10)


class RecipeStepsForm(forms.ModelForm):
    class Meta:
        model = RecipeSteps
        fields = ['step']
        widgets = {'step': forms.Textarea(
            attrs={'class': 'lbl-r l2-r q-ingredient', 'rows': '3'})}
        required = {
            'step': False,
        }


RecipeStepsFormSet = modelformset_factory(
    RecipeSteps, form=RecipeStepsForm, extra=5)
