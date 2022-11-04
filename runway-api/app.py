from os import environ as env
from flask import Flask

from dataset import dataset_api
from auth import auth_api
from test import test_api

APP = Flask(__name__)

APP.register_blueprint(auth_api)
APP.register_blueprint(dataset_api, url_prefix = '/api/datasets')
APP.register_blueprint(test_api, url_prefix = '/api/test')

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=env.get("PORT", 5000))