# Generated by Django 4.1.7 on 2023-04-27 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopia', '0011_chef_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHelp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopia.chef')),
            ],
        ),
    ]
