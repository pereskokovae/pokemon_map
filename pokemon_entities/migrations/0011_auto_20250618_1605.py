# Generated by Django 3.1 on 2025-06-18 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0010_auto_20250618_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemonentity',
            name='previous_evolution',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_evolution', to='pokemon_entities.pokemon', verbose_name='Предыдущая Эволюция'),
        ),
    ]
