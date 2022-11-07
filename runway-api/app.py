from os import environ as env
from flask import Flask, session, request
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_session import Session
from urllib.request import urlopen
from json import loads

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
DB_DRIVER = env.get("DB_DRIVER")
DB_SERVER = env.get("DB_SERVER")
DB_PORT = env.get("DB_PORT")
DB_NAME = env.get("DB_NAME")
DB_USER = env.get("DB_USER")
DB_PASS = env.get("DB_PASS")
DB_URI = f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

print(f"Checking/creating database {DB_URI}")
engine = create_engine(DB_URI, echo = env.get("FLASK_DEBUG") == "1")
if not database_exists(engine.url):
    create_database(engine.url)

app_db = SQLAlchemy()
ModelBase = declarative_base()

from models.dataset import Dataset, Datafile
from models.model import Model
from models.visualizations import DatasetVisualization, ModelVisualization

print("Initializing app db")
with app.app_context():
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app_db = SQLAlchemy(app)
    app_db.init_app(app)
    ModelBase.metadata.create_all(engine, checkfirst = True)

print("Registering API routes")
from auth_api import auth_api, get_token_auth_header
from datasets_api import datasets_api
from models_api import models_api

app.register_blueprint(auth_api)
app.register_blueprint(datasets_api, url_prefix = '/api/datasets')
app.register_blueprint(models_api, url_prefix = '/api/models')

print("Up and running!")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = env.get("PORT", 5000))

@app.before_request
def before_req_func():
    if session.get("user") is None:
        token = request.headers.get("Authorization", None)
        if token is not None:
            token = token.split()[1]
            userinfo = urlopen("https://" + env["AUTH0_DOMAIN"] + "/userinfo?access_token=" + token).read()
            session["user"] = loads(userinfo)["email"]