from django.shortcuts import render
import requests

def index(request, page=0):
    '''Génère le rendu de la page index'''
    if page==0:
      offset = 0
      previous = 0
    else:
      offset = page*10
    limit = 10
    i = 0
    
    #Vérifie s'il y a un ajout a l'équipe
    if (request.GET.get('submitToTeam')):
      team_name = request.GET.get('teams')
      pok_id = request.GET.get('pok_id')
      pok_name = request.GET.get('pok_name')
      add_to_team(team_name, pok_id, pok_name)
      
    #Vérifie s'il y a une recherche et génére le retour de la recherche
    if (request.GET.get('search')):
      name = request.GET.get('search')
      
      #Retour lorsque recherche trop courte
      if len(name) == 1:
        previous = -1
        next = 0
        data = {}
        is_search = -1
        context = {'pokemon_list': data , 'previous': previous , 'next' :next, 'search':is_search, 'teams':teams_list}
        return render(request, 'pokedex/index.html', context)
      
      name_list = get_name_searched_list(name)
      all_results = []
      for name in name_list:
        i+=1
        url_api = 'https://pokeapi.co/api/v2/pokemon/{}'.format(name)
        response = requests.get(url_api)
        all_data = response.json()
        pokemon_data={
        'pokemon_id': all_data['id'],
        'name': all_data['name'],
        'index':i,
        'teams':teams_list,
        'type': all_data["types"][0]["type"]["name"]
        }
        if str(pokemon_data['pokemon_id']) not in types:
          types[str(pokemon_data['pokemon_id'])] = pokemon_data['type']      
        all_results.append(pokemon_data)
      data = all_results
      next = 0
      previous = -1
      is_search = 1
      
    #Pas de recherche renvoie l'index par défault
    else:    
      url_api = 'https://pokeapi.co/api/v2/pokemon?offset={}&limit={}'.format(offset,limit)
      response = requests.get(url_api)
      results = response.json()['results']
      data = []
      next = page + 1
      previous = page - 1
      is_search = 0
      for pokemon in results:
        i+=1
        print(pokemon)
        pokemon_id = pokemon['url'].split('/')[-2]
        if pokemon_id not in types:
          url_api_poke = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(str(pokemon_id))
          response_poke = requests.get(url_api_poke)
          all_data_poke = response_poke.json()
          type_poke = all_data_poke["types"][0]["type"]["name"]
          types[pokemon_id] = type_poke
        else:
          type_poke = types[pokemon_id]
        data.append({'name': pokemon['name'], 'pokemon_id':pokemon_id, 'index':i, 'type': type_poke})
    context = {'pokemon_list': data , 'previous': previous , 'next' :next, 'search':is_search, 'teams':teams_list}
    return render(request, 'pokedex/index.html', context)
    
def detail(request, pokemon_id):
    '''Génére le rendu de la page Details'''
    
     #Vérifie s'il y a un ajout a l'équipe
    if (request.GET.get('submitToTeam')):
      team_name = request.GET.get('teams')
      print(team_name)
      pok_id = request.GET.get('pok_id')
      print(pok_id)
      pok_name = request.GET.get('pok_name')
      print(pok_name)
      add_to_team(team_name, pok_id, pok_name)
      
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
      'next_id': next_id,
      'teams':teams_list
    }
    print(response.json()['name'])
    return render(request, 'pokedex/detail.html', context=data)


def teams(request):
  '''Affiche la page teams'''
  #Vérifie si création d'une nouvelle équipe
  if(request.GET.get('submitNewTeam')):
    name= str(request.GET.get('teamName'))
    realName = verify_team_name(name)
    create_team(realName)
  
  #Vérifie si suppression d'équipe
  if(request.GET.get('deleteTeam')):
    name= str(request.GET.get('delTeamName'))
    delete_team(name)
  
  #Vérifie si suppression de pokémon
  if(request.GET.get('deletePokemon')):
    teamName = request.GET.get('teamName')
    slotIndex = request.GET.get('slotIndex')
    delete_pokemon_from_team(teamName, slotIndex)
  
  context = {'teams': teams_list}
  return render(request, 'pokedex/teams.html', context)
 
def add_to_team(team_name, pok_id, pok_name):
  '''Ajoute un pokémon dans l'équipe en argument'''
  for team in teams_list:
    if team['name'] == team_name:
      for pokemon in team['pokemons']:
        if pokemon['pokemon_id'] == 0:
          pokemon['pokemon_id']= pok_id
          pokemon['name'] = pok_name
          pokemon['types'] = types[pok_id]
          break
      break
  

def create_team(name):
  '''Créer une épique'''
  teams_list.append({'name':name, 'pokemons':[{'id_team':1, 'pokemon_id':0, 'name':'', 'types':''},
                                              {'id_team':2, 'pokemon_id':0, 'name':'', 'types':''},
                                              {'id_team':3, 'pokemon_id':0, 'name':'', 'types':''},
                                              {'id_team':4, 'pokemon_id':0, 'name':'', 'types':''},
                                              {'id_team':5, 'pokemon_id':0, 'name':'', 'types':''},
                                              {'id_team':6, 'pokemon_id':0,' name':'', 'types':''}]})

def delete_team(name):
  '''Supprime l'équipe dont le nom est en argument'''
  i=0
  team_index =0
  for team in teams_list:
    if team['name']==name:
      team_index = i
    i+=1
  teams_list.pop(team_index)

def delete_pokemon_from_team(teamName, slotIndex):
  """Supprime un pokémon de l'équipe en argument"""
  for team in teams_list:
    if team['name'] == teamName :
      for pokemon in team['pokemons']:
        if int(pokemon['id_team']) == int(slotIndex):
          pokemon['pokemon_id'] = 0
          pokemon['name'] = ''
          pokemon['types'] = ""
          break
      break
          
def verify_team_name(name):
    '''vérifie l'unicité du nom pour limité les erreurs'''
    if name == "":
      nb_teams = len(teams_list)
      name = "equipe" + str(nb_teams+1)
    for team in teams_list:
      if team['name']== name:
        name = name + '.1'
    return name

'''Liste des equipes'''
teams_list = list()

'''Dictionnaire des types pour accélérer l'app'''
types = dict()

'''Dictionnaire des noms pour la recherche'''
names = dict(A=
    ['Abomasnow',
    'Abra',
    'Absol',
    'Accelgor',
    'Aegislash',
    'Aerodactyl',
    'Aggron',
    'Aipom',
    'Alakazam',
    'Alcremie',
    'Alomomola',
    'Altaria',
    'Amaura',
    'Ambipom',
    'Amoonguss',
    'Ampharos',
    'Anorith',
    'Appletun',
    'Applin',
    'Araquanid',
    'Arbok',
    'Arcanine',
    'Arceus',
    'Archen',
    'Archeops',
    'Arctovish',
    'Arctozolt',
    'Ariados',
    'Armaldo',
    'Aromatisse',
    'Aron',
    'Arrokuda',
    'Articuno',
    'Audino',
    'Aurorus',
    'Avalugg',
    'Axew',
    'Azelf',
    'Azumarill',
    'Azurill'],
             B=[

'bagon',
'baltoy',
'banette',
'barbaracle',
'barboach',
'barraskewda',
'basculin-red-striped',
'bastiodon',
'bayleef',
'beartic',
'beautifly',
'beedrill',
'beheeyem',
'beldum',
'bellossom',
'bellsprout',
'bergmite',
'bewear',
'bibarel',
'bidoof',
'binacle',
'bisharp',
'blacephalon',
'blastoise',
'blaziken',
'blipbug',
'blissey',
'blitzle',
'boldore',
'boltund',
'bonsly',
'bouffalant',
'bounsweet',
'braixen',
'braviary',
'breloom',
'brionne',
'bronzong',
'bronzor',
'bruxish',
'budew',
'buizel',
'bulbasaur',
'buneary',
'bunnelby',
'burmy',
'butterfree',
'buzzwole'],
             C=[

'cacnea',
'cacturne',
'calyrex',
'camerupt',
'carbink',
'carkol',
'carnivine',
'carracosta',
'carvanha',
'cascoon',
'castform',
'caterpie',
'celebi',
'celesteela',
'centiskorch',
'chandelure',
'chansey',
'charizard',
'charjabug',
'charmander',
'charmeleon',
'chatot',
'cherrim',
'cherubi',
'chesnaught',
'chespin',
'chewtle',
'chikorita',
'chimchar',
'chimecho',
'chinchou',
'chingling',
'cinccino',
'cinderace',
'clamperl',
'clauncher',
'clawitzer',
'claydol',
'clefable',
'clefairy',
'cleffa',
'clobbopus',
'cloyster',
'coalossal',
'cobalion',
'cofagrigus',
'combee',
'combusken',
'comfey',
'conkeldurr',
'copperajah',
'corphish',
'corsola',
'corviknight',
'corvisquire',
'cosmoem',
'cosmog',
'cottonee',
'crabominable',
'crabrawler',
'cradily',
'cramorant',
'cranidos',
'crawdaunt',
'cresselia',
'croagunk',
'crobat',
'croconaw',
'crustle',
'cryogonal',
'cubchoo',
'cubone',
'cufant',
'cursola',
'cutiefly',
'cyndaquil'],
             D=[

'darkrai',
'darmanitan-standard',
'dartrix',
'darumaka',
'decidueye',
'dedenne',
'deerling',
'deino',
'delcatty',
'delibird',
'delphox',
'deoxys-normal',
'dewgong',
'dewott',
'dewpider',
'dhelmise',
'dialga',
'diancie',
'diggersby',
'diglett',
'ditto',
'dodrio',
'doduo',
'donphan',
'dottler',
'doublade',
'dracovish',
'dracozolt',
'dragalge',
'dragapult',
'dragonair',
'dragonite',
'drakloak',
'drampa',
'drapion',
'dratini',
'drednaw',
'dreepy',
'drifblim',
'drifloon',
'drilbur',
'drizzile',
'drowzee',
'druddigon',
'dubwool',
'ducklett',
'dugtrio',
'dunsparce',
'duosion',
'duraludon',
'durant',
'dusclops',
'dusknoir',
'duskull',
'dustox',
'dwebble'],
             E=[

'eelektrik',
'eelektross',
'eevee',
'eiscue-ice',
'ekans',
'eldegoss',
'electabuzz',
'electivire',
'electrike',
'electrode',
'elekid',
'elgyem',
'emboar',
'emolga',
'empoleon',
'entei',
'escavalier',
'espeon',
'espurr',
'eternatus',
'excadrill',
'exeggcute',
'exeggutor',
'exploud'],
             F=[

'falinks',
'farfetchd',
'fearow',
'feebas',
'fennekin',
'feraligatr',
'ferroseed',
'ferrothorn',
'finneon',
'flaaffy',
'flabebe',
'flapple',
'flareon',
'fletchinder',
'fletchling',
'floatzel',
'floette',
'florges',
'flygon',
'fomantis',
'foongus',
'forretress',
'fraxure',
'frillish',
'froakie',
'frogadier',
'froslass',
'frosmoth',
'furfrou',
'furret'],
             G=[
'gabite',
'gallade',
'galvantula',
'garbodor',
'garchomp',
'gardevoir',
'gastly',
'gastrodon',
'genesect',
'gengar',
'geodude',
'gible',
'gigalith',
'girafarig',
'giratina-altered',
'glaceon',
'glalie',
'glameow',
'glastrier',
'gligar',
'gliscor',
'gloom',
'gogoat',
'golbat',
'goldeen',
'golduck',
'golem',
'golett',
'golisopod',
'golurk',
'goodra',
'goomy',
'gorebyss',
'gossifleur',
'gothita',
'gothitelle',
'gothorita',
'gourgeist-average',
'granbull',
'grapploct',
'graveler',
'greedent',
'greninja',
'grimer',
'grimmsnarl',
'grookey',
'grotle',
'groudon',
'grovyle',
'growlithe',
'grubbin',
'grumpig',
'gulpin',
'gumshoos',
'gurdurr',
'guzzlord',
'gyarados'],
             H=[

'hakamo-o',
'happiny',
'hariyama',
'hatenna',
'hatterene',
'hattrem',
'haunter',
'hawlucha',
'haxorus',
'heatmor',
'heatran',
'heliolisk',
'helioptile',
'heracross',
'herdier',
'hippopotas',
'hippowdon',
'hitmonchan',
'hitmonlee',
'hitmontop',
'ho-oh',
'honchkrow',
'honedge',
'hoopa',
'hoothoot',
'hoppip',
'horsea',
'houndoom',
'houndour',
'huntail',
'hydreigon',
'hypno'],
             I=[

'igglybuff',
'illumise',
'impidimp',
'incineroar',
'indeedee-male',
'infernape',
'inkay',
'inteleon',
'ivysaur'],
             J=[

'jangmo-o',
'jellicent',
'jigglypuff',
'jirachi',
'jolteon',
'joltik',
'jumpluff',
'jynx'],
             K=[

'kabuto',
'kabutops',
'kadabra',
'kakuna',
'kangaskhan',
'karrablast',
'kartana',
'kecleon',
'keldeo-ordinary',
'kingdra',
'kingler',
'kirlia',
'klang',
'klefki',
'klink',
'klinklang',
'koffing',
'komala',
'kommo-o',
'krabby',
'kricketot',
'kricketune',
'krokorok',
'krookodile',
'kubfu',
'kyogre',
'kyurem'],
             L=[

'lairon',
'lampent',
'landorus-incarnate',
'lanturn',
'lapras',
'larvesta',
'larvitar',
'latias',
'latios',
'leafeon',
'leavanny',
'ledian',
'ledyba',
'lickilicky',
'lickitung',
'liepard',
'lileep',
'lilligant',
'lillipup',
'linoone',
'litleo',
'litten',
'litwick',
'lombre',
'lopunny',
'lotad',
'loudred',
'lucario',
'ludicolo',
'lugia',
'lumineon',
'lunala',
'lunatone',
'lurantis',
'luvdisc',
'luxio',
'luxray',
'lycanroc-midday'],
             M=[

'machamp',
'machoke',
'machop',
'magby',
'magcargo',
'magearna',
'magikarp',
'magmar',
'magmortar',
'magnemite',
'magneton',
'magnezone',
'makuhita',
'malamar',
'mamoswine',
'manaphy',
'mandibuzz',
'manectric',
'mankey',
'mantine',
'mantyke',
'maractus',
'mareanie',
'mareep',
'marill',
'marowak',
'marshadow',
'marshtomp',
'masquerain',
'mawile',
'medicham',
'meditite',
'meganium',
'melmetal',
'meloetta-aria',
'meltan',
'meowstic-male',
'meowth',
'mesprit',
'metagross',
'metang',
'metapod',
'mew',
'mewtwo',
'mienfoo',
'mienshao',
'mightyena',
'milcery',
'milotic',
'miltank',
'mime-jr',
'mimikyu-disguised',
'minccino',
'minior-red-meteor',
'minun',
'misdreavus',
'mismagius',
'moltres',
'monferno',
'morelull',
'morgrem',
'morpeko-full-belly',
'mothim',
'mr-mime',
'mr-rime',
'mudbray',
'mudkip',
'mudsdale',
'muk',
'munchlax',
'munna',
'murkrow',
'musharna'],
             N=[

'naganadel',
'natu',
'necrozma',
'nickit',
'nidoking',
'nidoqueen',
'nidoran-f',
'nidoran-m',
'nidorina',
'nidorino',
'nihilego',
'nincada',
'ninetales',
'ninjask',
'noctowl',
'noibat',
'noivern',
'nosepass',
'numel',
'nuzleaf'],
             O=[

'obstagoon',
'octillery',
'oddish',
'omanyte',
'omastar',
'onix',
'oranguru',
'orbeetle',
'oricorio-baile',
'oshawott'],
             P=[

'pachirisu',
'palkia',
'palossand',
'palpitoad',
'pancham',
'pangoro',
'panpour',
'pansage',
'pansear',
'paras',
'parasect',
'passimian',
'patrat',
'pawniard',
'pelipper',
'perrserker',
'persian',
'petilil',
'phanpy',
'phantump',
'pheromosa',
'phione',
'pichu',
'pidgeot',
'pidgeotto',
'pidgey',
'pidove',
'pignite',
'pikachu',
'pikipek',
'piloswine',
'pincurchin',
'pineco',
'pinsir',
'piplup',
'plusle',
'poipole',
'politoed',
'poliwag',
'poliwhirl',
'poliwrath',
'polteageist',
'ponyta',
'poochyena',
'popplio',
'porygon',
'porygon-z',
'porygon2',
'primarina',
'primeape',
'prinplup',
'probopass',
'psyduck',
'pumpkaboo-average',
'pupitar',
'purrloin',
'purugly',
'pyroar',
'pyukumuku'],
             Q=[

'quagsire',
'quilava',
'quilladin',
'qwilfish'],
             R=[

'raboot',
'raichu',
'raikou',
'ralts',
'rampardos',
'rapidash',
'raticate',
'rattata',
'rayquaza',
'regice',
'regidrago',
'regieleki',
'regigigas',
'regirock',
'registeel',
'relicanth',
'remoraid',
'reshiram',
'reuniclus',
'rhydon',
'rhyhorn',
'rhyperior',
'ribombee',
'rillaboom',
'riolu',
'rockruff',
'roggenrola',
'rolycoly',
'rookidee',
'roselia',
'roserade',
'rotom',
'rowlet',
'rufflet',
'runerigus'],
             S=[

'sableye',
'salamence',
'salandit',
'salazzle',
'samurott',
'sandaconda',
'sandile',
'sandshrew',
'sandslash',
'sandygast',
'sawk',
'sawsbuck',
'scatterbug',
'sceptile',
'scizor',
'scolipede',
'scorbunny',
'scrafty',
'scraggy',
'scyther',
'seadra',
'seaking',
'sealeo',
'seedot',
'seel',
'seismitoad',
'sentret',
'serperior',
'servine',
'seviper',
'sewaddle',
'sharpedo',
'shaymin-land',
'shedinja',
'shelgon',
'shellder',
'shellos',
'shelmet',
'shieldon',
'shiftry',
'shiinotic',
'shinx',
'shroomish',
'shuckle',
'shuppet',
'sigilyph',
'silcoon',
'silicobra',
'silvally',
'simipour',
'simisage',
'simisear',
'sinistea',
'sirfetchd',
'sizzlipede',
'skarmory',
'skiddo',
'skiploom',
'skitty',
'skorupi',
'skrelp',
'skuntank',
'skwovet',
'slaking',
'slakoth',
'sliggoo',
'slowbro',
'slowking',
'slowpoke',
'slugma',
'slurpuff',
'smeargle',
'smoochum',
'sneasel',
'snivy',
'snom',
'snorlax',
'snorunt',
'snover',
'snubbull',
'sobble',
'solgaleo',
'solosis',
'solrock',
'spearow',
'spectrier',
'spewpa',
'spheal',
'spinarak',
'spinda',
'spiritomb',
'spoink',
'spritzee',
'squirtle',
'stakataka',
'stantler',
'staraptor',
'staravia',
'starly',
'starmie',
'staryu',
'steelix',
'steenee',
'stonjourner',
'stoutland',
'stufful',
'stunfisk',
'stunky',
'sudowoodo',
'suicune',
'sunflora',
'sunkern',
'surskit',
'swablu',
'swadloon',
'swalot',
'swampert',
'swanna',
'swellow',
'swinub',
'swirlix',
'swoobat',
'sylveon'],
             T=[

'taillow',
'talonflame',
'tangela',
'tangrowth',
'tapu-bulu',
'tapu-fini',
'tapu-koko',
'tapu-lele',
'tauros',
'teddiursa',
'tentacool',
'tentacruel',
'tepig',
'terrakion',
'thievul',
'throh',
'thundurus-incarnate',
'thwackey',
'timburr',
'tirtouga',
'togedemaru',
'togekiss',
'togepi',
'togetic',
'torchic',
'torkoal',
'tornadus-incarnate',
'torracat',
'torterra',
'totodile',
'toucannon',
'toxapex',
'toxel',
'toxicroak',
'toxtricity-amped',
'tranquill',
'trapinch',
'treecko',
'trevenant',
'tropius',
'trubbish',
'trumbeak',
'tsareena',
'turtonator',
'turtwig',
'tympole',
'tynamo',
'type-null',
'typhlosion',
'tyranitar',
'tyrantrum',
'tyrogue',
'tyrunt'],
             U=[

'umbreon',
'unfezant',
'unown',
'ursaring',
'urshifu-single-strike',
'uxie'],
             V=[

'vanillish',
'vanillite',
'vanilluxe',
'vaporeon',
'venipede',
'venomoth',
'venonat',
'venusaur',
'vespiquen',
'vibrava',
'victini',
'victreebel',
'vigoroth',
'vikavolt',
'vileplume',
'virizion',
'vivillon',
'volbeat',
'volcanion',
'volcarona',
'voltorb',
'vullaby',
'vulpix'],
             W=[

'wailmer',
'wailord',
'walrein',
'wartortle',
'watchog',
'weavile',
'weedle',
'weepinbell',
'weezing',
'whimsicott',
'whirlipede',
'whiscash',
'whismur',
'wigglytuff',
'wimpod',
'wingull',
'wishiwashi-solo',
'wobbuffet',
'woobat',
'wooloo',
'wooper',
'wormadam-plant',
'wurmple',
'wynaut'],
             X=[

'xatu',
'xerneas',
'xurkitree'],
             Y=[

'yamask',
'yamper',
'yanma',
'yanmega',
'yungoos',
'yveltal'],
             Z=[

'zacian',
'zamazenta',
'zangoose',
'zapdos',
'zarude',
'zebstrika',
'zekrom',
'zeraora',
'zigzagoon',
'zoroark',
'zorua',
'zubat',
'zweilous',
'zygarde-50'
])    




def get_name_searched_list(search_name):
    '''Recherche les noms correspondant au pattern search_name et en renvois la liste'''
    first_letter = search_name[0].capitalize()
    name_list = names[first_letter]
    print(name_list)
    final_liste = [name.lower() for name in name_list if search_name.capitalize() in name.capitalize()]
    return final_liste