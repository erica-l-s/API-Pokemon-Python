import uuid
from flask import Flask, render_template, jsonify,request
import requests

app = Flask(__name__)

class Pokemon:
    def __init__(self, nome, tipo, peso, altura):
        self.nome = nome
        self.tipo = tipo
        self.peso = peso
        self.altura = altura

def obter_info_pokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        nome_pokemon = dados['name'].capitalize()
        tipos = [tipo['type']['name'].capitalize() for tipo in dados['types']]
        peso = dados['weight']
        altura = dados['height']
        return Pokemon(nome_pokemon, tipos, peso, altura)
    else:
        print("Pokémon não encontrado.")
        return None

class Usuario:
    def __init__(self, nome):
        self.nome = nome

class TimePokemon:
    def __init__(self, id, nome_time):
        self.id = id
        self.nome_time = nome_time
        self.pokemons = []
        self.usuarios = []

    def adicionar_pokemon(self, pokemon):
        if len(self.pokemons) < 6:
            self.pokemons.append(pokemon)
            print(f"{pokemon.nome} foi adicionado ao time {self.nome_time}.")
        else:
            print("O time já está completo. Não é possível adicionar mais pokémons.")

    def adicionar_usuario(self, usuario):
        self.usuarios.append(usuario)
        print(f"{usuario.nome} foi adicionado ao time {self.nome_time}.")

    def listar_pokemons(self):
        print(f"Time: {self.nome_time}")
        for pokemon in self.pokemons:
            print(f"Nome: {pokemon.nome}, Tipo(s): {', '.join(pokemon.tipo)}")

times = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/times', methods=['GET'])
def listar_times():
    return jsonify({time_id: [pokemon.__dict__ for pokemon in time.pokemons] for time_id, time in times.items()})

@app.route('/times/<id_time>', methods=['GET'])
def obter_time(id_time):
    if id_time in times:
        return jsonify([pokemon.__dict__ for pokemon in times[id_time].pokemons])
    else:
        return "Time não encontrado", 404

@app.route('/gerar_time', methods=['POST'])
def gerar_time():
    nome_usuario = request.form['nome_usuario']
    lista_pokemons = request.form.getlist('lista_pokemons')
    
    time_id = str(uuid.uuid4())
    time = TimePokemon(time_id, nome_usuario)
    usuario = Usuario(nome_usuario)
    time.adicionar_usuario(usuario)
    
    pokemons_time = []
    for nome_pokemon in lista_pokemons:
        pokemon = obter_info_pokemon(nome_pokemon)
        if pokemon:
            pokemons_time.append(pokemon)
            time.adicionar_pokemon(pokemon)
        else:
            return "Erro ao encontrar Pokémon", 400
    
    times[time_id] = time
    
    return f"Time gerado com sucesso! ID do time: {time_id}"

if __name__ == '__main__':
    app.run(debug=True)