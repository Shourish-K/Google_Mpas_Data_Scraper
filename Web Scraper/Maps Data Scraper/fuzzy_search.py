import requests
from urllib.parse import urlencode
from url_setup import Setup
from geocoding import Geocoding


class FuzzySearch(Setup):

    def __init__(self):
        super().__init__()

    def fuzzy_search(self) -> dict:
        encoded_query: str
        query = input("Please Enter your search: ")
        query_dict = {"address": query}
        encoded_query = urlencode(query_dict)
        query = encoded_query.split("=")
        encoded_query = query[1]

        place: str
        place = input("Please Enter a place: ")

        limit: int
        limit = int(input("Enter the limit: "))

        geocoding = Geocoding(place)
        position = geocoding.geocode()
        lat = position[0]
        lon = position[1]

        radius: int
        radius = int(input("Please Enter a radius: ")) * 1000

        params = {
            "key": self.api_key,
            "lat": lat,
            "lon": lon,
            "radius": radius,
            "limit": limit,
        }

        fuzzy_search_url = f"https://{self.base_url}/search/{self.version}/poiSearch/{encoded_query}.{self.ext}"

        response = requests.get(fuzzy_search_url, params=params)
        response.raise_for_status()
        response_data = response.json()
        return response_data
