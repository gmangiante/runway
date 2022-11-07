from flask import Blueprint, jsonify, session
from flask_cors import CORS
from app import app_db
from models.dataset import Dataset
from sqlalchemy import or_

datasets_api = Blueprint("datasets_api", __name__)
CORS(datasets_api, expose_headers=["Content-Type", "Authorization"], origins=['http://localhost:5173'])

@datasets_api.route("/list")
def list_datasets():
    user = session.get("user")
    if user is None:
        return jsonify(app_db.session.query(Dataset).filter(Dataset.is_public.is_(True)).all())
    else:
        return jsonify(app_db.session.query(Dataset).filter(or_(Dataset.is_public.is_(True), Dataset.created_by == user)).all())

@datasets_api.route("/create", methods = ["POST"])
def create_dataset():
    pass