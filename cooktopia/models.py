from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Chef(models.Model):
    name = models.CharField(max_length=200)
    followers = models.ManyToManyField("Chef")
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Comment(models.Model):
    title = models.CharField(max_length=200)
    chef = models.OneToOneField(Chef, on_delete=models.CASCADE)


class Ingridient(models.Model):
    title = models.CharField(max_length=200)

class Category(models.Model):
    title = models.CharField(max_length=200)
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    chef = models.OneToOneField(Chef, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)



class RecipeIngridient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE)
    ingridient = models.ForeignKey(
        Ingridient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('recipe', 'ingridient')
