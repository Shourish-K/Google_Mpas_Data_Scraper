from data_row import DataRow
from extended_search import ExtendedSearch


class DataCleaner:
    def __init__(self, data: dict):
        super().__init__()
        self.summary_data: dict = data["summary"]
        self.result_data: list = data["results"]
        self.data_row_list = []

    def set_data(self):
        seperator = " "
        num_of_results = int(self.summary_data["numResults"])
        query = str(self.summary_data["query"])
        lat = self.summary_data["geoBias"]["lat"]
        lon = self.summary_data["geoBias"]["lon"]
        geo_bias = (lat, lon)

        if num_of_results > 0:
            for index in range(0, len(self.result_data)):
                type_of_search = self.result_data[index]["type"]

                distance_from_geo_bias = float(round(self.result_data[index]["dist"], 2))

                poi_name = self.result_data[index]["poi"]["name"]

                if "phone" in self.result_data[index]["poi"]:
                    phone = self.result_data[index]["poi"]["phone"]
                else:
                    phone = None

                if "url" in self.result_data[index]["poi"]:
                    website = self.result_data[index]["poi"]["url"]
                else:
                    website = None

                if "categories" in self.result_data[index]["poi"]:
                    categories: list = self.result_data[index]["poi"]["categories"]
                    category = seperator.join(categories)
                else:
                    category = None

                if "position" in self.result_data[index]:
                    lat_pos = self.result_data[index]["position"]["lat"]
                    lon_pos = self.result_data[index]["position"]["lon"]
                    geo_position = (lat_pos, lon_pos)
                else:
                    geo_position = None

                address_list = []

                if "address" in self.result_data[index]:
                    address_list.append(poi_name)
                    if "streetName" in self.result_data[index]["address"]:
                        street_name = self.result_data[index]["address"]["streetName"]
                        address_list.append(street_name)

                    if "municipalitySubdivision" in self.result_data[index]["address"]:
                        municipality_sub_division = self.result_data[index]["address"]["municipalitySubdivision"]
                        address_list.append(municipality_sub_division)

                    if "municipality" in self.result_data[index]["address"]:
                        municipality = self.result_data[index]["address"]["municipality"]
                        address_list.append(municipality)

                    if "countrySubdivisionName" in self.result_data[index]["address"]:
                        country_sub_division_name = self.result_data[index]["address"]["countrySubdivisionName"]
                        address_list.append(country_sub_division_name)

                    if "country" in self.result_data[index]["address"]:
                        country = self.result_data[index]["address"]["country"]
                        address_list.append(country)

                    if "postalCode" in self.result_data[index]["address"]:
                        postal_code = self.result_data[index]["address"]["postalCode"]
                        address_list.append(postal_code)

                    address = seperator.join(address_list)
                else:
                    address = None

                if "dataSources" in self.result_data[index] and "poiDetails" in self.result_data[index]["dataSources"]:
                    data_source_id = self.result_data[index]["dataSources"]["poiDetails"][0]["id"]
                    data_source = ExtendedSearch()
                    poi_details = data_source.extended_search(data_source_id)
                    description = poi_details[0]
                    price_label = poi_details[1]
                    total_ratings = poi_details[2]
                    min_rating = poi_details[3]
                    max_rating = poi_details[4]
                    rating = poi_details[5]
                    social_media = poi_details[6]
                    social_media_url = poi_details[7]
                else:
                    description = None
                    price_label = None
                    total_ratings = None
                    min_rating = None
                    max_rating = None
                    rating = None
                    social_media = None
                    social_media_url = None

                new_data_row = DataRow(
                    type=type_of_search,
                    distance_from_geo_bias=distance_from_geo_bias,
                    poi_name=poi_name,
                    phone=phone,
                    website=website,
                    category=category,
                    geo_position=geo_position,
                    address=address,
                    description=description,
                    price_label=price_label,
                    total_ratings=total_ratings,
                    min_rating=min_rating,
                    max_rating=max_rating,
                    rating=rating,
                    social_media=social_media,
                    social_media_url=social_media_url
                )
                self.data_row_list.append(new_data_row)
            return self.data_row_list
        else:
            return "No Results Found"
