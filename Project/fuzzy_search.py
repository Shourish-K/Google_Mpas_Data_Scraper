import requests
from urllib.parse import urlencode
from url_setup import Setup
from geocoding import Geocoding


class FuzzySearch(Setup):

    def __init__(self):
        super().__init__()

    def fuzzy_search(self, search, location, search_limit, radius_meters) -> dict:
        encoded_query: str
        query = search
        query_dict = {"address": query}
        encoded_query = urlencode(query_dict)
        query = encoded_query.split("=")
        encoded_query = query[1]

        place: str
        place = location

        limit: int
        limit = search_limit

        geocoding = Geocoding(place)
        position = geocoding.geocode()
        lat = position[0]
        lon = position[1]

        radius: int
        radius = radius_meters * 1000

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
