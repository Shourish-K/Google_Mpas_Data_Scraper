from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import pandas
import os
from fuzzy_search import FuzzySearch
from data_cleaner import DataCleaner
from .models import SearchHistory
from . import db
views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("index.html", user=current_user)


@views.route("/data-scraper", methods=["GET", "POST"])
@login_required
def data_scraper():
    if request.method == "POST":
        query = request.form.get("query")
        file_name = request.form.get("filename")
        file_format = request.form.get("filetype")
        location = request.form.get("location")
        radius = request.form.get("radius")
        limit = request.form.get("limit")
        if location == "":
            location = current_user.default_location
        try:
            if radius == "":
                radius = 5
            else:
                radius = float(radius)
        except ValueError:
            flash("Please enter a numerical value for radius!", category="error")
            return redirect(url_for("views.data_scraper"))
        try:
            if limit == "":
                limit = 100
            else:
                limit = int(limit)
        except ValueError:
            flash("Please enter a integer value for radius!", category="error")
            return redirect(url_for("views.data_scraper"))
        if len(query) < 1:
            flash("Search must be at least 1 character long!", category="error")
        elif len(location) < 2:
            flash("Location must be at least 2 characters long!", category="error")
        elif len(file_name) < 2:
            flash("File name must be at least 2 characters long!", category="error")
        elif file_format == "default":
            flash("Please select a file format!", category="error")
        else:
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
            data = search.fuzzy_search(query, location, limit, radius)
            data_cleaner = DataCleaner(data)
            data_row_list = data_cleaner.set_data()

            if data_row_list != 0:
                geo_bias = data_row_list.pop()
                query = data_row_list.pop()
                num_of_results = data_row_list.pop()
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

                if file_format == "CSV":
                    if os.path.exists(f"D:/Final Year Project/Project/website/static/scraped-data/"
                                      f"{current_user.id}-{current_user.first_name}-"
                                      f"{current_user.last_name}/{file_name}.csv"):
                        flash("The file already exists please try another name!", category="error")
                    else:
                        with open(f"D:/Final Year Project/Project/website/static/scraped-data/"
                                  f"{current_user.id}-{current_user.first_name}-"
                                  f"{current_user.last_name}/{file_name}.csv", mode="w") as file:
                            data_frame.to_csv(file, index=False)
                            new_search = SearchHistory(
                                search=query,
                                geo_bias=geo_bias,
                                number_of_results=num_of_results,
                                path=f"/static/scraped-data/{current_user.id}-{current_user.first_name}-"
                                     f"{current_user.last_name}/{file_name}.csv",
                                user_id=current_user.id
                            )
                            db.session.add(new_search)
                            db.session.commit()
                        flash("Data scraped successfully!", category="success")
                else:
                    if os.path.exists(f"D:/Final Year Project/Project/website/static/scraped-data/"
                                      f"{current_user.id}-{current_user.first_name}-"
                                      f"{current_user.last_name}/{file_name}.xlsx"):
                        flash("The file already exists please try another name!", category="error")
                    else:
                        data_frame.to_excel(f"D:/Final Year Project/Project/website/static/scraped-data/"
                                            f"{current_user.id}-{current_user.first_name}-"
                                            f"{current_user.last_name}/{file_name}.xlsx", index=False)
                        new_search = SearchHistory(
                            search=query,
                            geo_bias=geo_bias,
                            number_of_results=num_of_results,
                            path=f"/static/scraped-data/"
                                 f"{current_user.id}-{current_user.first_name}-{current_user.last_name}/"
                                 f"{file_name}.xlsx",
                            user_id=current_user.id
                        )
                        db.session.add(new_search)
                        db.session.commit()
                        flash("Data scraped successfully!", category="success")
                        return render_template("searchhistory.html", user=current_user)
            else:
                flash("No results found!", category="error")
    return render_template("datascraper.html", user=current_user)


@views.route("/search-history", methods=["GET", "POST"])
@login_required
def search_history():
    return render_template("searchhistory.html", user=current_user)

@login_required
@views.route("/graph/<history_id>", methods=["GET", "POST"])
def abc(history_id):

    history = SearchHistory.query.filter_by(id=history_id).first()

    if "csv" in history.path:
        data = pandas.read_csv(f"website{history.path}")
    else:
        data = pandas.read_excel(f"website{history.path}")

    value1 = 0
    value2 = 0
    value3 = 0
    value4 = 0
    value5 = 0

    values = data["metersDistanceFromGeoBias"].tolist()

    for value in values:
        if 0 <= value < 2499.99:
            value1 += 1
        elif 2500 <= value < 4999.99:
            value2 += 1
        elif 5000 <= value < 7499.99:
            value3 += 1
        elif 7500 <= value < 9999.99:
            value4 += 1
        else:
            value5 += 1

    labels = ["0m to 2499.99m", "2500m to 4999.99m", "5000m to 7499.99m", "7500m to 9999.99m", "10000m+"]
    data_values = [value1, value2, value3, value4, value5]

    total = ((0+2500)/2)*value1+((2501+5000)/2)*value2+((5001+7500)/2)*value3+((7501+10000)/2)*value4+((20000)/2)*value5
    total_values = 0
    for num in data_values:
        total_values += num

    mean = total/total_values

    maximum = 0
    for num in values:
        if num > maximum:
            maximum = num

    minimum = 10000
    for num in values:
        if num < minimum:
            minimum = num


    category = data.category.value_counts()

    unique_category = []
    for i in data["category"]:
        if i not in unique_category:
            unique_category.append(i)


    return render_template("abc.html", title=f"{str(history.search).title()} Data Analysis", geo_bias_labels=labels,
                           geo_bias_values=data_values, user=current_user, geo_bias_mean=round(mean, 2), geo_bias_max=round(maximum, 2),
                           geo_bias_min=round(minimum, 2), name=str(history.search).title(), category_values=category.tolist(),
                           category_labels=unique_category)
