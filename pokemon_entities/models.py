from django.db import models
import datetime  # noqa F401


class Pokemon(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name="Идентификатор покемона")
    title = models.CharField(
        max_length=200,
        verbose_name="Имя покемона")
    title_en = models.CharField(
        max_length=200,
        verbose_name="Имя покемона на английском",
        null=True,
        blank=True)
    title_jp = models.CharField(
        max_length=200, 
        verbose_name="Имя покемона на японском",
        null=True, 
        blank=True)
    image = models.ImageField(upload_to='pokemons',
                              verbose_name="Картинка покемона",
                              blank=True,
                              null=True)
    description = models.TextField(verbose_name="Описание покемона", null=True)
    previous_evolution = models.ForeignKey(
        "self",
        verbose_name="Предыдущая Эволюция",
        on_delete=models.CASCADE,
        related_name='next_evolutions',
        null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name="Данные покемона",
        on_delete=models.CASCADE,
        default=1)
    lat = models.FloatField(verbose_name="Широта", null=True)
    lon = models.FloatField(verbose_name="Долгота", null=True)
    appeared_at = models.DateTimeField(
        verbose_name="Время появления",
        default=datetime.datetime.now)
    disappeared_at = models.DateTimeField(
        verbose_name="Время исчезания",
        default=datetime.datetime.now)
    level = models.IntegerField(verbose_name="Уровень", null=True)
    health = models.IntegerField(
        verbose_name="Здоровье",
        null=True,
        blank=True)
    strenght = models.IntegerField(
        verbose_name="Сила",
        null=True,
        blank=True)
    defence = models.IntegerField(
        verbose_name="Защита",
        null=True,
        blank=True)
    stamina = models.IntegerField(
        verbose_name="Выносливость",
        null=True,
        blank=True)


    def __str__(self):
        return f'{self.pokemon.title}'