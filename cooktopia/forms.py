from django import forms
from .models import Chef
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


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
            'name': forms.TextInput(attrs={'class': 'lbl-r l2-r', 'placeholder': 'Nome'}),
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
