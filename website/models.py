from datetime import datetime
from website import db
from flask_sqlalchemy import *
from base64 import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    top_progress = db.Column(db.String)
    full_progress = db.Column(db.Text)
    date_joined = db.Column(db.DateTime, default=datetime.now)
    about = db.Column(db.Text, default="")
    grade = db.Column(db.String, default="")
    image = db.Column(db.String, default=(
        "https://lh6.googleusercontent.com/-9-T7Yc3MUlU/AAAAAAAAAAI/AAAAAAAAAAA/CJDv3ZmEmkI/s64c"))
    admin = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<User {self.username}>"


# TODO: Fix data base
class Lesson(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    # goes_to = db.column(db.String)
    title = db.Column(db.String, unique=True)
    subtitle = db.Column(db.String, unique=True)
    img = db.Column(db.LargeBinary)
    body = db.Column(db.Text, unique=True)
    questions = db.Column(db.String)
    answers = db.Column(db.String)
    tags = db.Column(db.String)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.LargeBinary)
    date_created = db.Column(db.DateTime, default=datetime.now)


class Errors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String)
    error = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date_created = db.Column(db.DateTime, default=datetime.now)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
