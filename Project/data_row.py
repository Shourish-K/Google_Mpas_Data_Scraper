class DataRow:
    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self.distance_from_geo_bias = kwargs.get("distance_from_geo_bias")
        self.poi_name = kwargs.get("poi_name")
        self.phone = kwargs.get("phone")
        self.website = kwargs.get("website")
        self.category = kwargs.get("category")
        self.geo_position = kwargs.get("geo_position")
        self.address = kwargs.get("address")
        self.description = kwargs.get("description")
        self.price_label = kwargs.get("price_label")
        self.total_ratings = kwargs.get("total_ratings")
        self.min_rating = kwargs.get("min_rating")
        self.max_rating = kwargs.get("max_rating")
        self.rating = kwargs.get("rating")
        self.social_media = kwargs.get("social_media")
        self.social_media_url = kwargs.get("social_media_url")
