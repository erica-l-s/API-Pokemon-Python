from flask import Flask, jsonify, request, render_template
import requests
import uuid

app = Flask(__name__)

# Dicionário para armazenar os times criados
teams = {}

# Classe para representar um Pokémon
class Pokemon:
    def __init__(self, name, pokemon_id, height, weight):
        self.name = name
        self.id = pokemon_id
        self.height = height
        self.weight = weight

# Função para obter a lista de todos os Pokémon da API oficial do Pokémon
def get_pokemon_list():
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_list = [pokemon['name'].capitalize() for pokemon in data['results']]
        return pokemon_list
    else:
        return []

# Função para obter informações sobre um Pokémon da PokeAPI
def get_pokemon_info(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_id = data['id']
        height = data['height']
        weight = data['weight']
        return Pokemon(name.capitalize(), pokemon_id, height, weight)
    else:
        return None
    
# Rota para renderizar o HTML
@app.route('/')
def index():
    pokemon_options = get_pokemon_list()
    team_data = get_all_teams()
    return render_template('index.html', pokemon_options=pokemon_options, teams=team_data)

def get_all_teams():
    # Função para obter todos os times registrados
    teams_info = []
    for team in teams.values():
        team_info = {'user': team['user'], 'id': team['id'], 'pokemons': []}
        for pokemon in team['pokemons']:
            pokemon_info = {
                'name': pokemon['name'],
                'height': pokemon['height'],
                'weight': pokemon['weight']
            }
            team_info['pokemons'].append(pokemon_info)
        teams_info.append(team_info)
    return teams_info

# Rota para listar todos os times registrados
@app.route('/api/teams', methods=['GET'])
def get_teams():
    return jsonify(teams)

# Rota para buscar um time registrado por usuário
@app.route('/api/teams/<username>', methods=['GET'])
def get_team_by_username(username):
    if username in teams:
        return jsonify(teams[username])
    else:
        return jsonify({'error': 'Time não encontrado para o usuário especificado'}), 404

# Rota para criar um novo time ou adicionar Pokémon a um time existente
@app.route('/api/teams', methods=['POST'])
def create_team():
    data = request.form

    if 'user' not in data or 'pokemons[]' not in data:
        return jsonify({'error': 'Os campos user e pokemons são obrigatórios'}), 400

    username = data['user']
    pokemon_names = data.getlist('pokemons[]')

    # Verifica se o usuário já possui um time registrado
    if username in teams:
        team = teams[username]
        for pokemon_name in pokemon_names:
            # Verifica se o Pokémon já está na lista do time
            if pokemon_name not in [pokemon['name'] for pokemon in team['pokemons']]:
                pokemon_info = get_pokemon_info(pokemon_name)
                if pokemon_info:
                    team['pokemons'].append({
                        'name': pokemon_info.name,
                        'id': pokemon_info.id,
                        'height': pokemon_info.height,
                        'weight': pokemon_info.weight
                    })
                else:
                    return jsonify({'error': f'Pokémon não encontrado: {pokemon_name}'}), 400
            else:
                return jsonify({'error': f'O Pokémon {pokemon_name} já está na lista do time'}), 400
        return jsonify({'message': 'Pokémons adicionados ao time existente', 'team_id': team['id']}), 200
    else:
        # Se o usuário não possuir um time registrado, cria um novo time
        team_id = str(uuid.uuid4())
        team = {'id': team_id, 'user': username, 'pokemons': []}

        for pokemon_name in pokemon_names:
            pokemon_info = get_pokemon_info(pokemon_name)
            if pokemon_info:
                team['pokemons'].append({
                    'name': pokemon_info.name,
                    'id': pokemon_info.id,
                    'height': pokemon_info.height,
                    'weight': pokemon_info.weight
                })
            else:
                return jsonify({'error': f'Pokémon não encontrado: {pokemon_name}'}), 400

        teams[username] = team
        return jsonify({'message': 'Time criado com sucesso', 'team_id': team_id}), 201


if __name__ == '__main__':
    app.run(debug=True)





# import uuid
# from flask import Flask, request, render_template, jsonify
# import requests

# app = Flask(__name__)

# # Definição da classe Pokemon
# class Pokemon:
#     def __init__(self, nome, tipo, peso, altura):
#         self.nome = nome
#         self.tipo = tipo
#         self.peso = peso
#         self.altura = altura
        
#     def to_dict(self):
#         return {
#             'nome': self.nome,
#             'tipo': self.tipo,
#             'peso': self.peso,
#             'altura': self.altura
#         }
# # Função para obter uma lista de todos os Pokémon da API
# def obter_lista_pokemon():
#     url = "https://pokeapi.co/api/v2/pokemon?limit=1000"  # Define a URL para buscar todos os Pokémon
#     resposta = requests.get(url)

#     if resposta.status_code == 200:
#         dados = resposta.json()
#         lista_pokemon = [pokemon['name'].capitalize() for pokemon in dados['results']]
#         return lista_pokemon
#     else:
#         print("Erro ao obter lista de Pokémon.")
#         return []
    
# # Função para obter informações sobre um Pokémon da PokeAPI
# def obter_info_pokemon(nome):
#     url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
#     resposta = requests.get(url)

#     if resposta.status_code == 200:
#         dados = resposta.json()
#         nome_pokemon = dados['name'].capitalize()
#         tipos = [tipo['type']['name'].capitalize() for tipo in dados['types']]
#         peso = dados['weight']
#         altura = dados['height']
#         return Pokemon(nome_pokemon, tipos, peso, altura)
#     else:
#         print("Pokémon não encontrado.")
#         return None

# # Definição da classe Usuario
# class Usuario:
#     def __init__(self, nome):
#         self.nome = nome

# # Definição da classe TimePokemon
# class TimePokemon:
#     def __init__(self, id, nome_time):
#         self.id = id
#         self.nome_time = nome_time
#         self.pokemons = []
#         self.usuarios = []

#     def adicionar_pokemon(self, pokemon):
#         if len(self.pokemons) < 6:
#             self.pokemons.append(pokemon)
#             print(f"{pokemon.nome} foi adicionado ao time {self.nome_time}.")
#         else:
#             print("O time já está completo. Não é possível adicionar mais pokémons.")

#     def adicionar_usuario(self, usuario):
#         self.usuarios.append(usuario)
#         print(f"{usuario.nome} foi adicionado ao time {self.nome_time}.")

#     def listar_pokemons(self):
#         print(f"Time: {self.nome_time}")
#         for pokemon in self.pokemons:
#             print(f"Nome: {pokemon.nome}, Tipo(s): {', '.join(pokemon.tipo)}")

# # Dicionário para armazenar os times criados
# times = {}

# # Rota para a página inicial

# @app.route('/')
# def index():
#     # Passar os times com nome de usuário e Pokémon associados e a lista de Pokémon para o template
#     times_info = []
#     for time_id, time in times.items():
#         pokemons = [pokemon.nome for pokemon in time]
#         usuarios = [usuario.nome for usuario in time]
#         time_info = {
#             'id': time_id,
#             'usuario': usuarios,
#             'pokemons': pokemons
            
#         }
#         times_info.append(time_info)

#     lista_pokemon = obter_lista_pokemon()  # Obtém a lista de todos os Pokémon

#     return render_template('index.html', times_info=times_info, lista_pokemon=lista_pokemon)


# # Rota para gerar um novo time
# @app.route('/gerar_time', methods=['POST'])
# def gerar_time():
    
#     nome_time = request.form['nome_time']
#     lista_pokemons = request.form.getlist('lista_pokemons')
    
       
#     # Verifica se o nome do time já existe
#     for time_id, time in times.items():
#         if time.nome_time == nome_time:
#             for nome_pokemon in lista_pokemons:
#                 # Iterar sobre a lista de pokémons fornecida pelo usuário
#                 pokemon = obter_info_pokemon(nome_pokemon)
#                 if pokemon:
#                     time.adicionar_pokemon(pokemon)  # Adicionar o Pokémon ao time
#                 else:
#                     return "Erro ao encontrar Pokémon", 400  # Retornar erro se não encontrar o Pokémon
#             return f"Pokemons adicionados ao time {nome_time}", 200

#     # Se o nome do time não existir, criar um novo time
#     time_id = str(uuid.uuid4())  # Gerar um ID único para o time
#     novo_time = TimePokemon(time_id, nome_time)  # Criar um novo objeto TimePokemon
    
#     for nome_pokemon in lista_pokemons:
#         # Iterar sobre a lista de pokémons fornecida pelo usuário
#         pokemon = obter_info_pokemon(nome_pokemon)
#         if pokemon:
#             novo_time.adicionar_pokemon(pokemon)  # Adicionar o Pokémon ao time
#         else:
#             return "Erro ao encontrar Pokémon", 400  # Retornar erro se não encontrar o Pokémon
    
#     times[time_id] = novo_time  # Adicionar o time ao dicionário de times
    
#     return f"Time gerado com sucesso! ID do time: {time_id}", 200

# # Rota para listar todos os times registrados
# @app.route('/times', methods=['GET'])
# def listar_times():
#     times_json = {}
#     for time_id, pokemons in times.items():
#         times_json[time_id] = [pokemon.to_dict() for pokemon in pokemons]
#     return jsonify(times_json)

# # Rota para obter um time específico com base na ID única
# @app.route('/times/<id_time>', methods=['GET'])
# def obter_time(id_time):
#     if id_time in times:
#         return jsonify(times[id_time])  # Retornar o time se encontrado
#     else:
#         return "Time não encontrado", 404  # Retornar erro se o time não for encontrado

# if __name__ == '__main__':
#     app.run(debug=True)