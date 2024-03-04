from flask import Flask, jsonify, request, render_template
import requests
import uuid
from dataclasses import dataclass
from typing import List, Dict

app = Flask(__name__)

# Dicionário para armazenar os times criados
teams = {}

# Classe para representar um Pokémon
@dataclass
class Pokemon:
    name: str
    pokemon_id: int
    height: int
    weight: int

# Função para obter a lista de todos os Pokémon da API oficial do Pokémon
def get_pokemon_list() -> List[str]:
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
    response = requests.get(url)
    data = response.json() if response.status_code == 200 else {'results': []}
    return [pokemon['name'].capitalize() for pokemon in data['results']]

# Função para obter informações sobre um Pokémon da PokeAPI
def get_pokemon_info(name: str) -> Pokemon:
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return Pokemon(name.capitalize(), data['id'], data['height'], data['weight'])
    else:
        return None

# Rota para renderizar o HTML
@app.route('/')
def index():
    pokemon_options = get_pokemon_list()
    team_data = get_all_teams()
    return render_template('index.html', pokemon_options=pokemon_options, teams=team_data)

def get_all_teams() -> List[Dict]:
    # Função para obter todos os times registrados
    teams_info = []
    for team in teams.values():
        team_info = {'user': team['user'], 'id': team['id'], 'pokemons': []}
        for pokemon in team['pokemons']:
            pokemon_info = {
                'name': pokemon.name,
                'height': pokemon.height,
                'weight': pokemon.weight
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
    team = teams.get(username)
    if team:
        return jsonify(team)
    else:
        return jsonify({'error': 'Time nao encontrado para o usuario especificado'}), 404

# Rota para criar um novo time ou adicionar Pokémon a um time existente
@app.route('/api/teams', methods=['POST'])
def create_team():
    data = request.form
    username = data.get('user')
    pokemon_names = data.getlist('pokemons[]')

    if not username or not pokemon_names:
        return jsonify({'error': 'Os campos user e pokemons sao obrigatorios'}), 400

    team = teams.get(username)
    if team:
        for pokemon_name in pokemon_names:
            if pokemon_name not in [pokemon.name for pokemon in team['pokemons']]:
                pokemon_info = get_pokemon_info(pokemon_name)
                if pokemon_info:
                    team['pokemons'].append(pokemon_info)
                else:
                    return jsonify({'error': f'Pokemon nao encontrado: {pokemon_name}'}), 400
            else:
                return jsonify({'error': f'O Pokemon {pokemon_name} já esta na lista do time'}), 400
        return jsonify({'message': f'Pokemons adicionados ao time existente', 'team_id': team['id']}), 200
    else:
        team_id = str(uuid.uuid4())
        new_team = {'id': team_id, 'user': username, 'pokemons': []}
        for pokemon_name in pokemon_names:
            pokemon_info = get_pokemon_info(pokemon_name)
            if pokemon_info:
                new_team['pokemons'].append(pokemon_info)
            else:
                return jsonify({'error': f'Pokemon nao encontrado: {pokemon_name}'}), 400
        teams[username] = new_team
        return jsonify({'message': f'Time {username} criado com sucesso', 'team_id': team_id}), 201

if __name__ == '__main__':
    app.run(debug=True)
