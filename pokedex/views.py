from django.shortcuts import render
import requests
from django.http import HttpResponse


def index(request, page=0):
    if page==0:
      offset = 0
      previous = 0
    else:
      offset = page*20
    limit = 20
    url_api = 'https://pokeapi.co/api/v2/pokemon?offset={}&limit={}'.format(offset,limit)
    response = requests.get(url_api)
    results = response.json()['results']
    data = []
    next = page + 1
    previous = page - 1
    for pokemon in results:
      print(pokemon)
      pokemon_id = pokemon['url'].split('/')[-2]
      url_api_poke = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(str(pokemon_id))
      response_poke = requests.get(url_api_poke)
      all_data_poke = response_poke.json()
      type_poke = all_data_poke["types"][0]["type"]["name"]
      data.append({'name': pokemon['name'], 'pokemon_id':pokemon_id, 'type': type_poke})
    context = {'pokemon_list': data , 'previous': previous , 'next' :next}
    return render(request, 'pokedex/index.html', context)
    
def detail(request, pokemon_id):
    url_api ='https://pokeapi.co/api/v2/pokemon/{}/'.format(str(pokemon_id))
    response = requests.get(url_api)
    all_data = response.json()
    types = []
    previous_id = pokemon_id -1
    next_id = pokemon_id +1
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
      'previous_id': previous_id,
      'next_id': next_id
    }
    print(response.json()['name'])
    return render(request, 'pokedex/detail.html', context=data)
