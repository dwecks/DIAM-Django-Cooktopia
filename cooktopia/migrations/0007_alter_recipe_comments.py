# Generated by Django 4.1.7 on 2023-04-21 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopia', '0006_remove_recipe_recipesteps_recipesteps_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='comments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cooktopia.comment'),
        ),
    ]