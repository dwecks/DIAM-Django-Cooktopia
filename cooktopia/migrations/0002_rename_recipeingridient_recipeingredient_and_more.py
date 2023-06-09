# Generated by Django 4.1.7 on 2023-04-21 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopia', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipeIngridient',
            new_name='RecipeIngredient',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='MealType',
            new_name='mealType',
        ),
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='ingridient',
            new_name='ingredient',
        ),
        migrations.AlterUniqueTogether(
            name='recipeingredient',
            unique_together={('recipe', 'ingredient')},
        ),
    ]
