from url_setup import Setup
import requests


class ExtendedSearch(Setup):
    def __init__(self):
        super().__init__()
        self.description = None
        self.price_label = None
        self.total_ratings = None
        self.min_rating = None
        self.max_rating = None
        self.rating = None
        self.social_media = None
        self.social_media_url = None
        self.poi_details = []

    def extended_search(self, data_source_id: str) -> list:
        params = {
            "key": self.api_key,
            "id": data_source_id
        }
        extended_search_url = f"https://{self.base_url}/search/{self.version}/poiDetails.{self.ext}"
        response = requests.get(extended_search_url, params=params)
        response.raise_for_status()
        poi_details_result_data = response.json()["result"]
        if "description" in poi_details_result_data:
            self.description = poi_details_result_data["description"]

        if "priceRange" in poi_details_result_data:
            self.price_label = poi_details_result_data["priceRange"]["label"]

        if "rating" in poi_details_result_data:
            self.total_ratings = poi_details_result_data["rating"]["totalRatings"]
            self.rating = poi_details_result_data["rating"]["value"]
            self.min_rating = poi_details_result_data["rating"]["minValue"]
            self.max_rating = poi_details_result_data["rating"]["maxValue"]

        if "socialMedia" in poi_details_result_data:
            self.social_media = poi_details_result_data["socialMedia"][0]["name"]
            self.social_media_url = poi_details_result_data["socialMedia"][0]["url"]

        self.poi_details.extend(
            [
                self.description,
                self.price_label,
                self.total_ratings,
                self.min_rating,
                self.max_rating,
                self.rating,
                self.social_media,
                self.social_media_url
            ]
        )
        return self.poi_details
