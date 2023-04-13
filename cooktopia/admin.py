from django.contrib import admin
from .models import Chef, Comment, Ingridient, Recipe, RecipeIngridient
# Register your models here.

admin.site.register(Chef)
admin.site.register(Comment)
admin.site.register(Ingridient)
admin.site.register(Recipe)
admin.site.register(RecipeIngridient)
