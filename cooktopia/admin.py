from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Chef)
admin.site.register(Comment)
admin.site.register(Ingridient)
admin.site.register(MealType)
admin.site.register(Difficulty)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeSteps)
admin.site.register(ChefFollower)
