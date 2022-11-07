from flask import Blueprint, jsonify, session, request
from flask_cors import CORS
from app import app_db
from models.dataset import Dataset
from sqlalchemy import or_
from auth_api import requires_auth
from json import loads

datasets_api = Blueprint("datasets_api", __name__)
CORS(datasets_api, supports_credentials = True, expose_headers=["Content-Type", "Authorization"], origins=['http://localhost:5173'])

@datasets_api.route("/", methods = ["GET"])
def list_datasets():
    user = session.get("user")
    if user is None:
        return jsonify(app_db.session.query(Dataset).filter(Dataset.is_public.is_(True)).all())
    else:
        return jsonify(app_db.session.query(Dataset).filter(or_(Dataset.is_public.is_(True), Dataset.created_by == user)).all())

@datasets_api.route("/", methods = ["POST"])
@requires_auth
def create_dataset():
    ds_dict = loads(request.data)
    ds_dict.pop("id", None)
    ds = Dataset(**ds_dict)
    app_db.session.add(ds)
    app_db.session.commit()
    return jsonify({ "new_dataset_id": ds.id })

@datasets_api.route("/<id>", methods = ["GET"])
def get_dataset_detail(id):
    return jsonify(app_db.session.query(Dataset).filter(Dataset.id == id).one())
