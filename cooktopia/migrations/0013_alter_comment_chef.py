# Generated by Django 4.1.7 on 2023-04-30 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopia', '0012_remove_recipe_comments_comment_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='chef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopia.chef'),
        ),
    ]
