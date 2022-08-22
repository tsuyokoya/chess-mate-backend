from flask import Flask, redirect, request, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from models import db, connect_db, User, Stat

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    return "home"
