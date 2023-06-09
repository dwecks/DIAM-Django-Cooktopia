# Generated by Django 4.1.7 on 2023-04-25 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopia', '0009_category_alter_recipe_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chef',
            name='followers',
        ),
        migrations.CreateModel(
            name='ChefFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='cooktopia.chef')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='cooktopia.chef')),
            ],
        ),
    ]
