from urllib.parse import urlencode
import requests

API_KEY = "AIzaSyCIkOTJrFnkZTNEVIcaErvj8CEh3FBjJmA"
data_type = "json"
params = {
    "address": "1600 Amphitheatre Parkway, Mountain View, CA",
    "key": API_KEY
}
url_params = urlencode(params)
endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
url = f"{endpoint}?{url_params}"

print(url)
response = requests.get(url)
response.raise_for_status()
print(response.json())
