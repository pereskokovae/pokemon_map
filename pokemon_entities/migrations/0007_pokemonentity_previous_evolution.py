# Generated by Django 3.1 on 2025-06-15 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20250614_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='previous_evolution',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemonentity'),
        ),
    ]
