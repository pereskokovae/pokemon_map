import folium
import json


from django.utils import timezone
from .models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_entity = PokemonEntity.objects.filter(appeared_at__lt=timezone.localtime(), disappeared_at__gt=timezone.localtime())
    for pokemon in pokemons_entity:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.image:
            img_url = pokemon.image.url
        else:
            img_url = None

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title
        })


    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    entities = pokemon.entities.all()
    for entity in entities:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.image.url)
            )
       
    previous_evolution = {}
    next_evolution = {}
    if pokemon.previous_evolution:
        title_previous_evolution = pokemon.previous_evolution.title
        id_previous_evolution = pokemon.previous_evolution.id
        image_url_previous_evolution = request.build_absolute_uri(pokemon.previous_evolution.image.url)
          
        evolution = pokemon.previous_evolution.next_evolutions.first()
        title_next_evolution = evolution.title
        id_next_evolution = evolution.id
        image_url_next_evolution = request.build_absolute_uri(evolution.image.url)
    else:
        title_previous_evolution = None
        id_previous_evolution = None
        image_url_previous_evolution = None
        title_next_evolution = None
        id_next_evolution = None
        image_url_next_evolution = None

    previous_evolution.update({
        "title_ru": title_previous_evolution,
        "pokemon_id": id_previous_evolution,
        "img_url": image_url_previous_evolution
        })

    next_evolution.update({
        "title_ru": title_next_evolution,
        "pokemon_id": id_next_evolution,
        "img_url": image_url_next_evolution
        })

    pokemon = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": request.build_absolute_uri(pokemon.image.url),
        "previous_evolution": previous_evolution,
        "next_evolution": next_evolution
        }
   
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
