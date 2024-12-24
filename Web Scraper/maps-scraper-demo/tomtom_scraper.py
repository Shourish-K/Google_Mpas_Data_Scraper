from urllib.parse import urlencode
import requests

API_KEY = "ASGVdi71XD5yoczPxJThAWsCGG5Kt2ar"
EXT = "json"
BASE_URL = "api.tomtom.com"
VERSION = 2


def poi_search():
    query = input("Please Enter your search:")
    query_dict = {"address": query}
    encoded_query = urlencode(query_dict)
    query = encoded_query.split("=")
    encoded_query = query[1]

    poi_search_url = f"https://{BASE_URL}/search/{VERSION}/poiSearch/{encoded_query}.{EXT}?key={API_KEY}&limit=3"
    print(poi_search_url)

    response = requests.get(url=poi_search_url)
    response.raise_for_status()
    print(response.json())


def fuzzy_search():
    query = input("Please Enter your search:")
    query_dict = {"address": query}
    encoded_query = urlencode(query_dict)
    query = encoded_query.split("=")
    encoded_query = query[1]
    params = {
        "key": API_KEY,
        "radius": 5000,
        "limit": 3,
    }
    fuzzy_search_url = f"https://{BASE_URL}/search/{VERSION}/search/{encoded_query}.{EXT}"
    print(fuzzy_search_url)

    response = requests.get(url=fuzzy_search_url, params=params)
    print(response.url)
    response.raise_for_status()
    print(response.json())


def extended_search(data_source_id: str):
    extended_search_url = f"https://{BASE_URL}/search/{VERSION}/poiDetails.{EXT}?key={API_KEY}&id={data_source_id}"
    response = requests.get(url=extended_search_url)
    response.raise_for_status()
    print(extended_search_url)
    print(response.json())


def geocoding():
    place = input("Please Enter a place:")
    query_dict = {"address": place}
    encoded_query = urlencode(query_dict)
    query = encoded_query.split("=")
    encoded_query = query[1]
    geocoding_url = f"https://{BASE_URL}/search/{VERSION}/geocode/{encoded_query}.{EXT}?key={API_KEY}"
    response = requests.get(geocoding_url)
    lat = response.json()["results"][0]["position"]["lat"]
    lon = response.json()["results"][0]["position"]["lon"]
    position = (lat, lon)
    print(position)


# fuzzy_search()
extended_search("Rm91cnNxdWFyZTo1NTM3ODlmYjQ5OGU4YmMxZTQwYmQwM2Y=")
