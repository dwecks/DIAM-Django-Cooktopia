# Generated by Django 4.1.7 on 2023-04-21 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopia', '0004_rename_ingredient_id_recipeingredient_ingredient_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeSteps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipeSteps',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='cooktopia.recipesteps'),
            preserve_default=False,
        ),
    ]
