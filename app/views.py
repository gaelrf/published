from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
from datetime import date, datetime

def index(request):
    return render(request, "index.html")

def get_data_from_api(request):
    url = "https://api.jolpi.ca/ergast/f1/seasons/"  # URL de la API
    response = requests.get(url)  # Realiza la petición GET
    if response.status_code == 200:
        data = response.json()  # Convierte la respuesta a JSON
        return JsonResponse(data)  # Devuelve los datos como respuesta JSON
    else:
        return JsonResponse({'error': 'Error al obtener los datos'}, status=response.status_code)

def get_seasons(request):
    url = "https://api.jolpi.ca/ergast/f1/seasons.json?limit=100&offset=0"  # URL de la API
    response = requests.get(url)  # Realiza la petición GET
    if response.status_code == 200:
        data = response.json()  # Convierte la respuesta a JSON
        seasons = data.get("MRData", {}).get("SeasonTable", {}).get("Seasons", [])
        return render(request, "seasons.html", {"seasons": seasons})
    else:
        return render(request, "error.html", {"error": "Error al obtener los datos"})

def circuits(request):
    url = "https://api.jolpi.ca/ergast/f1/circuits.json?limit=100&offset=0"  # URL de la API
    response = requests.get(url)  # Realiza la petición GET
    if response.status_code == 200:
        data = response.json()  # Convierte la respuesta a JSON
        circuits = data.get("MRData", {}).get("CircuitTable", {}).get("Circuits", [])
        return render(request, "circuits.html", {"circuits": circuits})
    else:
        return render(request, "error.html", {"error": "Error al obtener los datos"})

def standings(request, season):
    driver_url = f"https://api.jolpi.ca/ergast/f1/{season}/driverstandings/"
    constructor_url = f"https://api.jolpi.ca/ergast/f1/{season}/constructorstandings/"

    driver_response = requests.get(driver_url)
    constructor_response = requests.get(constructor_url)

    driver_standings = []
    constructor_standings = []

    if driver_response.status_code == 200:
        driver_data = driver_response.json()
        driver_standings = driver_data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])[0].get("DriverStandings", [])

    if constructor_response.status_code == 200:
        constructor_data = constructor_response.json()
        constructor_standings = constructor_data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])[0].get("ConstructorStandings", [])

    context = {
        'season': season,
        'driver_standings': driver_standings,
        'constructor_standings': constructor_standings
    }

    return render(request, 'standings.html', context)

def races(request, season):
    url = f"https://api.jolpi.ca/ergast/f1/{season}/races.json?limit=100&offset=0"  # API endpoint for season races
    response = requests.get(url)  # Perform GET request

    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])

        # Convert race dates to datetime.date objects
        for race in races:
            if 'date' in race:
                race['date'] = datetime.strptime(race['date'], "%Y-%m-%d").date()

        today = date.today()  # Get today's date
        return render(request, "season_races.html", {"races": races, "season": season, "today": today})
    else:
        return render(request, "error.html", {"error": "Error fetching races for the season"})

def circuit_races(request, circuit_id):
    url = f"https://api.jolpi.ca/ergast/f1/circuits/{circuit_id}/races.json?limit=100&offset=0"  # API endpoint for circuit races
    response = requests.get(url)  # Perform GET request
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])

        # Convert race dates to datetime.date objects
        for race in races:
            if 'date' in race:
                race['date'] = datetime.strptime(race['date'], "%Y-%m-%d").date()

        today = date.today()  # Get today's date
        return render(request, "circuits_races.html", {"races": races, "circuit_id": circuit_id, "today": today})
    else:
        return render(request, "error.html", {"error": "Error fetching races for the circuit"})

def race_results(request, season, round):
    url = f"https://api.jolpi.ca/ergast/f1/{season}/{round}/results/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        race_data = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])[0]  # Extract race data
        return render(request, "race_results.html", {"race": race_data})
    else:
        return render(request, "error.html", {"error": "Failed to fetch race results"})
