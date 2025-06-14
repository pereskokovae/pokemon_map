from django.db import models
import datetime  # noqa F401


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null=True, blank=True)
    title_jp = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='pokemons', blank=True, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=1)
    previous_evolution = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, default=None)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    appeared_at = models.DateTimeField(default=datetime.datetime.now)
    disappeared_at = models.DateTimeField(default=datetime.datetime.now)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True, blank=True)
    strenght = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f'{self.pokemon.title}'