# Generated by Django 3.1 on 2025-06-11 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_pokemon_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Lat', models.FloatField()),
                ('Lon', models.FloatField()),
            ],
        ),
    ]
