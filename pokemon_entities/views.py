import folium
import json


from django.utils import timezone
from .models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
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
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon

            if requested_pokemon:
                previous_evolution = {
                        "title_ru": requested_pokemon.title,
                        "pokemon_id": requested_pokemon.id,
                        "img_url": request.build_absolute_uri(requested_pokemon.image.url)
                }
 
            next_evolutions = requested_pokemon.next_evolutions.all()
            for evolution in next_evolutions:
                next_evolution = {
                    "title_ru": evolution.title,
                    "pokemon_id": evolution.id,
                    "img_url": request.build_absolute_uri(evolution.image.url)
                }

            entities = requested_pokemon.pokemons.all()
            for entity in entities:
                add_pokemon(
                    folium_map, entity.lat,
                    entity.lon,
                    request.build_absolute_uri(entity.pokemon.image.url)
                )

            pokemon = {
                    "pokemon_id": requested_pokemon.id,
                    "title_ru": requested_pokemon.title,
                    "title_en": requested_pokemon.title_en,
                    "title_jp": requested_pokemon.title_jp,
                    "description": requested_pokemon.description,
                    "img_url": request.build_absolute_uri(requested_pokemon.image.url),
                    "previous_evolution": previous_evolution,
                    "next_evolution": next_evolution
                    }
    
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
