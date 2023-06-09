# Generated by Django 4.1.7 on 2023-04-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopia', '0007_alter_recipe_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='chef',
            name='photo',
            field=models.ImageField(null=True, upload_to='profile'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='recipes'),
        ),
    ]
