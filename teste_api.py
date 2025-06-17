import pytest
import httpx

BASE_URL = "https://pokeapi.co/api/v2"

@pytest.mark.suite1
def teste_pokemon_valido():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/ditto")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "ditto"
        print("Pokémon encontrado:", data["name"], "ID:", data["id"], "Tipos:", [type_["type"]["name"] for type_ in data["types"]])

def teste_pokemon_invalido():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/ditto123")
        assert response.status_code == 404

def teste_get_pokemon_list():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0

        # Exibe os 20 primeiros Pokémon da lista
        print("Os 20 primeiros pokemons:", [pokemon['name'] for pokemon in data["results"][:20]])

def teste_pokemon_por_id():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        print("Pokémon ID 1:", data["name"], "Tipos:", [type_["type"]["name"] for type_ in data["types"]])

def teste_pokemon_por_type():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/type/1")
        assert response.status_code == 200
        data = response.json()
        assert "pokemon" in data
        assert len(data["pokemon"]) > 0 
        print("20 pokémons do tipo 1:", [pokemon["pokemon"]["name"] for pokemon in data["pokemon"][:20]])
