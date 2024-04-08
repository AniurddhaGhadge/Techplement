import time
import requests
import argparse
import json


WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = "9a4a9cde15aa28c113af30cef25854db"  

FAVORITES_FILE = "favorites.json" 

def load_favorites():
    try:
        with open(FAVORITES_FILE, "r") as f:
            favorites = json.load(f)
    except FileNotFoundError:
        favorites = []
    return favorites

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f)

def get_weather_by_city(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve weather data. Please try again later.")
        return None


def display_weather(weather_data):
    if weather_data:
        print("\nWeather Information:")
        print(f"City: {weather_data['name']}")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Weather: {weather_data['weather'][0]['description']}")
    else:
        print("No weather data available.")


def add_favorite(city, favorites):
    if city not in favorites:
        favorites.append(city)
        save_favorites(favorites)
        print(f"{city} added to favorites.")
        return True
    else:
        print(f"{city} is already in favorites.")
        return False


def remove_favorite(city, favorites):
    if city in favorites:
        favorites.remove(city)
        save_favorites(favorites)
        print(f"{city} removed from favorites.")
        return True
    else:
        print(f"{city} is not in favorites.")
        return False


def list_favorites(favorites):
    print("\nFavorite Cities:")
    if favorites:
        for index, city in enumerate(favorites, start=1):
            print(f"{index}. {city}")
    else:
        print("No favorite cities.")


def main():
    parser = argparse.ArgumentParser(description="Weather Checking Application")
    parser.add_argument("city", nargs="?", help="City name for weather checking")
    parser.add_argument("-a", "--add", help="Add city to favorites")
    parser.add_argument("-r", "--remove", help="Remove city from favorites")
    parser.add_argument("-c", "--list", action="store_true", help="List favorite cities")
    args = parser.parse_args()

    favorites = load_favorites() 

    
    if args.add:
        add_favorite(args.add, favorites)
    elif args.remove:
        remove_favorite(args.remove, favorites)
    elif args.list:
        list_favorites(favorites)
    else:
        if args.city:
            
            weather_data = get_weather_by_city(args.city)
            display_weather(weather_data)
        else:
            print("No command specified. Use -h or --help for usage information.")


if __name__ == "__main__":
    main()
