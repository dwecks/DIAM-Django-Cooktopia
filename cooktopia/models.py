from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Chef(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="profile", null=True)
    followers = models.ManyToManyField("Chef")
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Comment(models.Model):
    description = models.CharField(max_length=200)
    chef = models.OneToOneField(Chef, on_delete=models.CASCADE)


class Ingridient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MealType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Difficulty(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=200)
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="recipes", null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.DO_NOTHING)
    preparationTime = models.DecimalField(max_digits=3, decimal_places=0)
    mealType = models.ForeignKey(MealType, on_delete=models.DO_NOTHING)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comments = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)


class RecipeSteps(models.Model):
    step = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, null=True,  on_delete=models.CASCADE)

    def __str__(self):
        return self.step


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingridient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('recipe', 'ingredient')
