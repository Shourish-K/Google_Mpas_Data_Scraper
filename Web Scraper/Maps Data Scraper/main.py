import pandas
from fuzzy_search import FuzzySearch
from data_cleaner import DataCleaner

type_list = []
distance_from_geo_bias_list = []
poi_name_list = []
phone_list = []
website_list = []
category_list = []
geo_position_list = []
address_list = []
description_list = []
price_label_list = []
total_ratings_list = []
min_rating_list = []
max_rating_list = []
rating_list = []
social_media_list = []
social_media_url_list = []

formatted_data = {}

search = FuzzySearch()
data = search.fuzzy_search()
data_cleaner = DataCleaner(data)
data_row_list = data_cleaner.set_data()

try:
    for data_row in data_row_list:
        type_list.append(data_row.type)
        distance_from_geo_bias_list.append(data_row.distance_from_geo_bias)
        poi_name_list.append(data_row.poi_name)
        phone_list.append(data_row.phone)
        website_list.append(data_row.website)
        category_list.append(data_row.category)
        geo_position_list.append(data_row.geo_position)
        address_list.append(data_row.address)
        description_list.append(data_row.description)
        price_label_list.append(data_row.price_label)
        total_ratings_list.append(data_row.total_ratings)
        min_rating_list.append(data_row.min_rating)
        max_rating_list.append(data_row.max_rating)
        rating_list.append(data_row.rating)
        social_media_list.append(data_row.social_media)
        social_media_url_list.append(data_row.social_media_url)
except AttributeError:
    print(data_row_list)

formatted_data["resultType"] = type_list
formatted_data["metersDistanceFromGeoBias"] = distance_from_geo_bias_list
formatted_data["poiName"] = poi_name_list
formatted_data["phone"] = phone_list
formatted_data["website"] = website_list
formatted_data["category"] = category_list
formatted_data["geoPosition"] = geo_position_list
formatted_data["address"] = address_list
formatted_data["description"] = description_list
formatted_data["priceLabel"] = price_label_list
formatted_data["totalRatings"] = total_ratings_list
formatted_data["minRating"] = min_rating_list
formatted_data["maxRating"] = max_rating_list
formatted_data["rating"] = rating_list
formatted_data["socialMedia"] = social_media_list
formatted_data["socialMediaUrl"] = social_media_url_list

data_frame = pandas.DataFrame(formatted_data)
with open("scraped data.csv", mode="w") as file:
    data_frame.to_csv(file, index=False)
