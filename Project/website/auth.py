from flask import Blueprint, render_template, flash, request, redirect, url_for
from . import db, mail
import os
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from geocoding import Geocoding
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message
import re


auth = Blueprint("auth", __name__)
serializer = URLSafeTimedSerializer("qwertyuiopasdfghjklzxcvbnm")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if user.email_authenticated:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("views.home"))
                else:
                    flash("Incorrect Password, try again!", category="error")
            else:
                db.session.delete(user)
                db.session.commit()
                flash("User isn't verified, please signup again!", category="error")
        else:
            flash("Email doesn't exist, please sign up!", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        default_location = request.form.get("defaultLocation")

        user = User.query.filter_by(email=email).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            flash("User already exists, please login to access!", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters!", category="error")
        elif len(first_name) < 2:
            flash("First Name must be greater than 1 characters!", category="error")
        elif len(last_name) < 2:
            flash("Last Name must be greater than 1 characters!", category="error")
        elif password != confirm_password:
            flash("Passwords don't match!", category="error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters long!", category="error")
        elif len(default_location) < 2:
            flash("Default location must be at least 2 characters long!", category="error")
        else:

            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password, method="sha256"),
                default_location=default_location
            )
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(email=email).first()

            token = serializer.dumps(email, salt="email-confirm")
            msg = Message("Confirm Email - Maps Scraper", sender="mapsscraper@gmail.com", recipients=[email])
            link = url_for("auth.confirm_email", token=token, user_id=user.id, _external=True)
            msg.html = render_template("emailconfirmmail.html", name=first_name, confirm_link=link)
            mail.send(msg)
            flash("We have sent a verification email to your registered email address!", category="info")
            return redirect(url_for("auth.login"))

    return render_template("signup.html", user=current_user)


@auth.route("/confirm-email/<token>/<user_id>")
def confirm_email(token, user_id):
    user = User.query.filter_by(id=user_id).first()
    try:
        if user.email_authenticated:
            flash("You are already verified!", category="warning")
        else:
            email = serializer.loads(token, salt="email-confirm", max_age=120)
            user.email_authenticated = True
            db.session.commit()
            path = f"D:/Final Year Project/Project/website/static/scraped-data"
            directory = f"{user.id}-{user.first_name}-{user.last_name}"
            os.chdir(path)
            os.mkdir(directory)
            flash("User verification successful!", category="success")
    except SignatureExpired:
        if not user.email_authenticated:
            db.session.delete(user)
            db.session.commit()
            flash("The verification time has expired, please signup again!", category="error")
        else:
            flash("You are already verified!", category="warning")
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    flash("Logged out successfully!", category="success")
    logout_user()
    return redirect(url_for("auth.login"))
