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
        return jsonify({'error': 'Time nao encontrado para o usuario especificado'}), 404

# Rota para criar um novo time ou adicionar Pokémon a um time existente
@app.route('/api/teams', methods=['POST'])
def create_team():
    data = request.form

    if 'user' not in data or 'pokemons[]' not in data:
        return jsonify({'error': 'Os campos user e pokemons sao obrigatorios'}), 400

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
                    return jsonify({'error': f'Pokemon nao encontrado: {pokemon_name}'}), 400
            else:
                return jsonify({'error': f'O Pokemon {pokemon_name} já esta na lista do time'}), 400
        return jsonify({'message': f'Pokemon {pokemon_name} adicionado ao time existente', 'team_id': team['id']}), 200
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
                return jsonify({'error': f'Pokemon nao encontrado: {pokemon_name}'}), 400

        teams[username] = team
        return jsonify({'message': f'Time {username} criado com sucesso', 'team_id': team_id}), 201


if __name__ == '__main__':
    app.run(debug=True)
