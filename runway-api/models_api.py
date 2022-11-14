from flask import Blueprint, jsonify, session, request
from flask_cors import CORS
from app import app_db
from auth_api import requires_auth
from json import loads, dumps
from models.model import Model
from sqlalchemy import or_
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
from models.model import ModelDatafileAssociation
from models.dataset import Datafile
import pandas as pd
from io import StringIO
from flask_sse import sse
from multiprocessing import Process
import time
from datetime import datetime

models_api = Blueprint('models_api', __name__)

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
    model_dict.pop("dataset_name", None)
    model_dict.pop("fit_at", None)
    model_dict.pop("created_at", None)
    model_dict.pop("updated_at", None)
    model_dict['train_score'] = 0
    model_dict['val_score'] = 0
    datafiles = model_dict.pop("datafiles", None)
    model = Model(**model_dict)
    model_class = globals()[model_dict['class_name']]
    if type(model_dict['params']) == str:
        params = loads(model_dict['params'])
    else:
        params = model_dict['params']
    model_instance = model_class(**params)
    model.params = model_instance.get_params()
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
    for assoc in model.datafiles:
        app_db.session.delete(assoc)
    app_db.session.delete(model)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@models_api.route("sharing/<id>/<is_public>", methods = ["POST"])
@requires_auth
def set_sharing(id, is_public):
    model = app_db.session.get(Model, id)
    model.is_public = True if is_public == "true" else False
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

    sse.publish({'model_id': model.id}, type = "start", channel = "model_fit")
    
    fit_process = Process(
        target = run_fit(model.id, model.name, model.created_by, model_instance, X_train, y_train, X_val, y_val),
        daemon = True
    )
    fit_process.start()

    return dumps({'success': True }), 200, {'Content-Type':'application/json'}

def run_fit(model_id, name, created_by, model, X_train, y_train, X_val, y_val):
    model.fit(X_train, y_train)
    train_score = round(model.score(X_train, y_train), 4)
    val_score = round(model.score(X_val, y_val), 4)
    model_data = app_db.session.get(Model, model_id)
    model_data.train_score = train_score
    model_data.val_score = val_score
    model_data.fit_at = datetime.now()
    app_db.session.commit()
    time.sleep(3)
    sse.publish({'model_id': model_id, 'name': name, 'created_by': created_by, 'fit_at': model_data.fit_at,  'train_score': train_score,
        'val_score': val_score}, type = "complete", channel = "model_fit")