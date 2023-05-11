# Generated by Django 4.1.7 on 2023-05-11 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=30)),
                ('photo', models.ImageField(null=True, upload_to='profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ingridient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MealType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(null=True, upload_to='recipes')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=200)),
                ('preparationTime', models.DecimalField(decimal_places=0, max_digits=3)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('url', models.CharField(max_length=300)),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopia.chef')),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cooktopia.difficulty')),
                ('mealType', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cooktopia.mealtype')),
            ],
        ),
        migrations.CreateModel(
            name='UserHelp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopia.chef')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeSteps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.CharField(max_length=200)),
                ('recipe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cooktopia.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopia.chef')),
                ('recipe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cooktopia.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='ChefFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='cooktopia.chef')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='cooktopia.chef')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopia.ingridient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopia.recipe')),
            ],
            options={
                'unique_together': {('recipe', 'ingredient')},
            },
        ),
    ]
