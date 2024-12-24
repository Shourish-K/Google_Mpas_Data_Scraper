import requests
from urllib.parse import urlencode
from url_setup import Setup


class Geocoding(Setup):
    def __init__(self, place: str):
        super().__init__()
        self.place = place
        self.position: tuple = ()

    def geocode(self) -> tuple:
        query_dict = {"address": self.place}
        encoded_query = urlencode(query_dict)
        query = encoded_query.split("=")
        encoded_query = query[1]
        params = {
            "key": self.api_key
        }
        geocoding_url = f"https://{self.base_url}/search/{self.version}/geocode/" \
                        f"{encoded_query}.{self.ext}"
        response = requests.get(geocoding_url, params=params)
        response.raise_for_status()
        try:
            lat = response.json()["results"][0]["position"]["lat"]
            lon = response.json()["results"][0]["position"]["lon"]
        except IndexError:
            lat = 19.0760
            lon = 72.8777
        self.position = (lat, lon)
        return self.position
