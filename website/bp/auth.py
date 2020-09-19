from werkzeug.security import *
from flask import Blueprint, request, render_template, redirect, url_for
from website import app, db, login_manager, mail
from website.models import User
from flask_login import login_user, logout_user, login_required, current_user
from secrets import compare_digest
from flask_wtf import RecaptchaField
from flask_mail import Message
# from website import csrf
login_manager.login_view = 'home'

auth = Blueprint('auth', __name__, root_path=None)

rude_words = ["rude", "bad", "sucks", "suck", "hacker", "scks", "hcker"]


@auth.route("/register", methods=["GET", "POST"], endpoint="signup")
@auth.route("/sign_up", methods=["GET", "POST"], endpoint="signup")
@auth.route("/sign-up", methods=["GET", "POST"], endpoint="signup")
@auth.route("/signup", methods=["GET", "POST"], endpoint="signup")
def signup():
    recaptcha = RecaptchaField()
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        confirm_password = request.form["confirm-password"]
        about = request.form["about"]
        email = request.form["email"]
        letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        letters = list(letters)
        if username == "":
            return render_template("signup.html", error="*You did not enter any username.", confirm=confirm_password,
                                   username=username, password=password, about=about)
        elif len(username.split(" ")) > 1:
            return render_template("signup.html", error="*Your username cannot contain any spaces.",
                                   confirm=confirm_password, username=username, password=password, about=about,
                                   recaptcha=recaptcha)
        elif compare_digest(confirm_password, password):
            return render_template("signup.html", error="*Your passwords do not match.", confirm=confirm_password,
                                   username=username, password=password, about=about,
                                   recaptcha=recaptcha)
        elif compare_digest(password, ""):
            return render_template("signup.html", error="*You did not enter a password", confirm=confirm_password,
                                   username=username, password=password, about=about,
                                   recaptcha=recaptcha)
        elif bool(User.query.filter_by(username=username).first()):
            return render_template("signup.html", error="*The username is already taken.", confirm=confirm_password,
                                   username=username, password=password, about=about,
                                   recaptcha=recaptcha)
        elif username.lower in rude_words:
            return render_template("signup.html", error="*Rude words are not allowed.", confirm=confirm_password,
                                   username=username, password=password, about=about,
                                   recaptcha=recaptcha)
        else:
            for char in username:
                if char not in letters:
                    return render_template("signup.html", error="*Your username can only contain letters and numbers. ",
                                           confirm=confirm_password, username=username, password=password, about=about,
                                           recaptcha=recaptcha)
            i = 0
            for char in username:
                if char in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
                    i = i + 1
            if i < 4:
                return render_template("signup.html", error="*Your username must contain at least 4 letters.",
                                       confirm=confirm_password, username=username, password=password, about=about,
                                       recaptcha=recaptcha)
            for user in User.query.all():
                if user.username.lower() == username.lower():
                    return render_template("signup.html", error="*The username is already taken.",
                                           confirm=confirm_password, username=username, password=password, about=about,
                                           recaptcha=recaptcha)
            user = User()
            user.username = username
            user.top_progress = ""
            user.password = generate_password_hash(password)
            user.admin = 0
            user.email=email
            db.session.add(user)
            db.session.commit()
            login_user(User.query.filter_by(password=password, username=username).first(), remember=True)
            user_id = current_user.id
            profile = User()
            profile.user_id = user_id
            profile.about = about
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        return render_template("signup.html", error="", username="", password="", confirm="", about="",
                               recaptcha=recaptcha)


@auth.route("/sign_in", methods=["GET", "POST"], endpoint="login")
@auth.route("/sign-in", methods=["GET", "POST"], endpoint="login")
@auth.route("/signin", methods=["GET", "POST"], endpoint="login")
@auth.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        user = User.query.filter_by(password=password, username=username).first()
        if user is None:
            return render_template("login.html", error="*Incorrect username or password", username=username,
                                   password=password)
        else:
            login_user(user, remember=True)
            return redirect("/")
    else:
        return render_template("login.html", error="", text="", password="")


@auth.route("/signout", endpoint="logout")
@auth.route("/sign_out", endpoint="logout")
@auth.route("/log_out", endpoint="logout")
@auth.route("/logout", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect("/", code=302)


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    error = ''
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username)
        if user.email is None:
            error = "There is no email associated with your account."
        else:
            msg = Message("Password Reset for Coding for Kidz",
                          sender="passwordreset@coding-for-kidz.herokuapp.com",
                          recipients=[user.email])
            msg.body = "Dear " + user.username + " ,\nYou can reset your password at this link. This link will expire in 24 hours. If you did not request a password reset you can safely ignore the email.\nThanks,\nThe Coding for Kidz team"
            msg.html = "Dear " + user.username + " ,<br><br>You can reset your password here. This link will expire in 24 hours. If you did not request a password reset you can safely ignore the email.<br><br>Thanks,<br><br>The Coding for Kidz team"
            mail.send(msg)
    else:
        return render_template("forgotpassword.html", error=error)
