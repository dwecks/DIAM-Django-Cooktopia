from rest_framework import serializers
from .models import Recipe, Chef


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id', 'name', 'country')


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'title', "pub_date", 'description',
                  "preparationTime", "rating",  "chef")
