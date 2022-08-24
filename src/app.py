from flask import Flask, redirect, request, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from models import db, connect_db, User, Stat
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.route("/login", methods=["POST"])
@cross_origin()
def login_user():
    return "login"


@app.route("/signup", methods=["POST"])
@cross_origin()
def signup_user():
    username = request.json["username"]
    password = request.json["password"]
    res = User.register(username, password)
    return res
