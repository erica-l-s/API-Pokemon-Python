# Flask API for Pokémon Teams with Docker

This repository contains a Flask API that allows users to create and manage Pokémon teams. The API interacts with the official Pokémon API to retrieve information about Pokémon.

## Requirements
- Python 3.6 or higher
- Flask
- Requests
- Docker (for containerization)

## Features
- Create new Pokémon teams
- Add Pokémon to existing teams
- View all registered Pokémon teams
- Error handling for invalid Pokémon names and missing user input

## Installation
1. Clone the repository:

```
git clone https://github.com/yourusername/API-Pokemon-Python.git
```
2. Navigate to the project directory:

```
cd python-pokemon
```

3. Install the required Python packages:

```
pip install -r requirements.txt
```

## Usage
To run the Flask API, execute the following command in your terminal:

```
python app.py
```

This will start the Flask development server. 
You can access the API at *http://localhost:5000.*

## Endpoints
- GET /: Renders the HTML interface for creating and viewing Pokémon teams.
- GET /api/teams: Retrieves all registered teams.
- GET /api/teams/{username}: Retrieves a team by username.
- POST /api/teams: Creates a new team or adds Pokémon to an existing team.

## Docker
This project also includes a Dockerfile for containerization. To build a Docker image and run the container, follow these steps:

1. Build the Docker image:

```
docker build -t pokemon-api .
```
2. Run the Docker container:

``` 
docker run --rm -p 5000:5000 pokemon-api
```

The Flask API will be accessible at *http://localhost:5000* within the Docker container.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
