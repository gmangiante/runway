from flask import Blueprint, jsonify, session, request
from flask_cors import CORS
from app import app_db
from auth_api import requires_auth
from json import loads, dumps
from models.model import Model
from sqlalchemy import or_
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
from models.model import ModelDatafileAssociation
from models.dataset import Datafile
import pandas as pd
from io import StringIO

models_api = Blueprint('models_api', __name__)
CORS(models_api, supports_credentials = True, expose_headers=["Content-Type", "Authorization"], origins=['http://localhost:5173', 'http://localhost:5174'])

@models_api.route("/", methods = ["GET"])
def list_models():
    user = session.get("user")
    if user is None:
        return [model.serialize() for model in app_db.session.query(Model).filter(Model.is_public.is_(True)).all()], 200, {'Content-Type':'application/json'} 
    else:
        return [model.serialize() for model in app_db.session.query(Model).filter(or_(Model.is_public.is_(True), Model.created_by == user)).all()], 200, {'Content-Type':'application/json'} 

@models_api.route("/<id>", methods = ["GET"])
def get_model_detail(id):
    result = app_db.session.get(Model, id)
    return dumps(result.serialize()), 200, {'Content-Type':'application/json'} 

@models_api.route("/", methods = ["POST"])
@requires_auth
def create_model():
    model_dict = loads(request.data)
    model_dict.pop("id", None)
    datafiles = model_dict.pop("datafiles", None)
    model = Model(**model_dict)
    model_class = globals()[model_dict['class_name']]
    model_instance = model_class(**model_dict['params'])
    model.saved_model = pickle.dumps(model_instance)
    for file in datafiles:
        assoc = ModelDatafileAssociation(role = file['role'])
        assoc.model = model
        df = app_db.session.get(Datafile, file['datafile_id'])
        assoc.datafile = df
        model.datafiles.append(assoc)
        df.models.append(assoc)
    app_db.session.add(model)
    app_db.session.commit()
    return dumps({'success': True, 'new_model_id': model.id}), 200, {'Content-Type':'application/json'}

@models_api.route("/<id>", methods = ["DELETE"])
@requires_auth
def delete_model(id):
    model = app_db.session.get(Model, id)
    app_db.session.delete(model)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@models_api.route("/fit/<id>", methods = ["POST"])
@requires_auth
def fit_model(id):
    model = app_db.session.get(Model, id)
    
    train_file_id, val_file_id = -1, -1
    for file in model.datafiles:
        if file.role == "trainAndValidation":
            train_file_id = val_file_id = file.datafile_id
            break
        elif file.role == "train":
            train_file_id = file.datafile_id
        elif file.role == "validation":
            val_file_id = file.datafile_id
    if train_file_id == -1 or val_file_id == -1:
        return dumps({'success': False}), 200, {'Content-Type':'application/json'}
    train_file = app_db.session.get(Datafile, train_file_id)
    if train_file_id == val_file_id:
        if train_file.content_type == "text/csv":
            df = pd.read_csv(StringIO(train_file.content.decode()))
        X = df[model.feature_names]
        y = df[model.target_name]
        X_train, X_val, y_train, y_val = train_test_split(X, y)
    else:
        if train_file.content_type == "text/csv":
            df = pd.read_csv(StringIO(train_file.content.decode()))
            X_train = df[model.feature_names]
            y_train = df[model.target_names]
        val_file = app_db.session.get(Datafile, val_file_id)
        if val_file.content_type == "text/csv":
            df = pd.read_csv(StringIO(val_file.content.decode()))
            X_val = df[model.feature_names]
            y_val = df[model.target_names]

    model_instance = pickle.loads(model.saved_model)

    model_instance.fit(X_train, y_train)
    return dumps({'success': True, 'train_score': model_instance.score(X_train, y_train),
        'val_score': model_instance.score(X_val, y_val)}), 200, {'Content-Type':'application/json'}