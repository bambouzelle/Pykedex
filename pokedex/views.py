from django.shortcuts import render
import requests
from django.http import HttpResponse


def index(request):
    offset = 0
    limit = 20
    url_api = 'https://pokeapi.co/api/v2/pokemon?offset={}&limit={}'.format(offset,limit)
    response = requests.get(url_api)
    results = response.json()['results']
    data = []
    for pokemon in results:
      print(pokemon)
      pokemon_id = pokemon['url'].split('/')[-2]
      data.append({'name': pokemon['name'], 'pokemon_id':pokemon_id})
    context = {'pokemon_list': data }
    return render(request, 'pokedex/index.html', context)
    
def detail(request, pokemon_id):
    url_api ='https://pokeapi.co/api/v2/pokemon/{}/'.format(str(pokemon_id))
    response = requests.get(url_api)
    all_data = response.json()
    types = []
    for type in all_data['types']:
      types.append(type['type']['name'])
    data={
      'base_experience': all_data['base_experience'],
      'height' : all_data['height'],
      'weight' : all_data['weight'],
      'id': all_data['id'],
      'name': all_data['name'],
      'types':types,
      'sprite_default_front':all_data['sprites']['front_default'],
      'sprite_default_back':all_data['sprites']['back_default'],
      'sprite_shiny_front':all_data['sprites']['front_shiny'],
      'sprite_shiny_back':all_data['sprites']['back_shiny'],
    }
    print(response.json()['name'])
    return render(request, 'pokedex/detail.html', context=data)
