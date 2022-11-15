from flask import Blueprint, jsonify, session, request
from flask_cors import CORS
from app import app_db
from auth_api import requires_auth
from json import loads, dumps
from models.model import Model
from sqlalchemy import or_
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
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
from sklearn import metrics

models_api = Blueprint('models_api', __name__)

@models_api.route("/", methods = ["GET"])
def list_models():
    """
    List all models, filtering by user if available (otherwise returns only public)
    """
    user = session.get("user")
    if user is None:
        return [model.serialize() for model in app_db.session.query(Model).filter(Model.is_public.is_(True)).all()], 200, {'Content-Type':'application/json'} 
    else:
        return [model.serialize() for model in app_db.session.query(Model).filter(or_(Model.is_public.is_(True), Model.created_by == user)).all()], 200, {'Content-Type':'application/json'} 

@models_api.route("/<id>", methods = ["GET"])
def get_model_detail(id):
    """
    Get model detail by ID
    """
    result = app_db.session.get(Model, id)
    return dumps(result.serialize()), 200, {'Content-Type':'application/json'} 

@models_api.route("/", methods = ["POST"])
@requires_auth
def create_model():
    """
    Create new model from JSON spec (requires auth)
    Also constructs a model instance to save pickled version
    """
    model_dict = loads(request.data)
    
    # Get rid of the stuff we want the database to auto-fill
    # (left over if this model is a duplicate)
    model_dict.pop("id", None)
    model_dict.pop("dataset_name", None)
    model_dict.pop("fit_at", None)
    model_dict.pop("created_at", None)
    model_dict.pop("updated_at", None)
    model_dict['train_score'] = 0
    model_dict['val_score'] = 0

    # Capture the datafiles in their original JSON format
    # And then get rid of them from the dict
    datafiles = model_dict.pop("datafiles", None)

    # Build the Model, set the class (must be imported above)
    # Reconstruct the params (may be JSON object or string, depending on source)
    # Construct the model instance with the params and pickle it
    model = Model(**model_dict)
    model_class = globals()[model_dict['class_name']]
    if type(model_dict['params']) == str:
        params = loads(model_dict['params'])
    else:
        params = model_dict['params']
    model_instance = model_class(**params)
    model.params = model_instance.get_params()
    model.saved_model = pickle.dumps(model_instance)

    # Save the datafile associations for this model
    # Needs "no_autoflush" to avoid trying to commit with outstanding operations
    with app_db.session.no_autoflush:
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
    """
    Delete a model by ID (requires auth)
    """
    model = app_db.session.get(Model, id)
    for assoc in model.datafiles:
        app_db.session.delete(assoc)
    app_db.session.delete(model)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@models_api.route("sharing/<id>/<is_public>", methods = ["POST"])
@requires_auth
def set_sharing(id, is_public):
    """
    Set model sharing to public or private by ID (requires auth)
    """
    model = app_db.session.get(Model, id)
    model.is_public = True if is_public == "true" else False
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@models_api.route("/<id>/download", methods = ["GET"])
@requires_auth
def download_model(id):
    """
    Download pickled version of model (requires auth)
    """
    model = app_db.session.get(Model, id)
    return model.saved_model, 200, {'Content-Type':'application/octet-stream'}

@models_api.route("/fit/<id>", methods = ["POST"])
@requires_auth
def fit_model(id):
    """
    Fit the model!
    Expects the associated datafiles to either be a single trainAndValidation file
    (uses default train-test split for now)
    or 1 train file and 1 validation file
    Uses Process to spawn a new thread so it can return to the user immediately
    Also publishes a "start" model fit event via SSE
    """
    model = app_db.session.get(Model, id)
    
    # Locate our train and validation files
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
        # this shouldn't happen!
        return dumps({'success': False}), 200, {'Content-Type':'application/json'}
    train_file = app_db.session.get(Datafile, train_file_id)

    # Construct target and features
    # train-test split if same file, otherwise use 2 separate files with overlapping columns
    if train_file_id == val_file_id:
        if train_file.content_type == "text/csv":
            df = pd.read_csv(StringIO(train_file.content.decode()))
        X = df[model.feature_names]
        y = df[model.target_name]
        # if it's a classifier, we should stratify!
        stratify = y if model.class_name in ['LogisticRegression', 'GradientBoostingClassifier'] else None
        X_train, X_val, y_train, y_val = train_test_split(X, y, stratify = stratify)
    else:
        if train_file.content_type == "text/csv":
            df = pd.read_csv(StringIO(train_file.content.decode()))
            X_train = df[model.feature_names]
            y_train = df[model.target_name]
        val_file = app_db.session.get(Datafile, val_file_id)
        if val_file.content_type == "text/csv":
            df = pd.read_csv(StringIO(val_file.content.decode()))
            X_val = df[model.feature_names]
            y_val = df[model.target_name]

    # Load the saved model and get going!
    model_instance = pickle.loads(model.saved_model)

    sse.publish({'model_id': model.id}, type = "start", channel = "model_fit")
    
    fit_process = Process(
        target = run_fit(model.id, model.name, model.created_by, model_instance, X_train, y_train, X_val, y_val),
        daemon = True
    )
    fit_process.start()

    return dumps({'success': True }), 200, {'Content-Type':'application/json'}

def run_fit(model_id, name, created_by, model, X_train, y_train, X_val, y_val):
    """
    The spawned fitting thread
    Currently only handles sklearn models (fit/score/predict)
    Always returns primary train and validation score, along with fit stats
    Also retrieves other scores and post-fit attributes as appropriate per model class
    Publishes completion to server-side event
    """
    fit_start = time.perf_counter()
    model.fit(X_train, y_train)
    fit_end = time.perf_counter()
    train_score = round(model.score(X_train, y_train), 4)
    val_score = round(model.score(X_val, y_val), 4)
    model_data = app_db.session.get(Model, model_id)
    model_data.train_score = train_score
    model_data.val_score = val_score
    model_data.fit_at = datetime.now()
    model_data.fit_time_ms = round((fit_end - fit_start) * 1000)
    model_data.other_scores = get_other_scores(model_data.class_name, model, X_val, y_val)
    model_data.other_attribs = get_other_attribs(model_data.class_name, model)
    app_db.session.commit()
    # artificial delay for demo
    time.sleep(3)
    sse.publish({'model_id': model_id, 'name': name, 'created_by': created_by, 'fit_at': model_data.fit_at, 'fit_time_ms': model_data.fit_time_ms,  'train_score': train_score,
        'val_score': val_score, 'other_scores': model_data.other_scores, 'other_attribs': model_data.other_attribs}, type = "complete", channel = "model_fit")

def get_other_scores(class_name, model_instance, X_val, y_val):
    """
    Return post-fit scores as appropriate per model class
    Expects model class name, actual model instance, and validation data
    """
    y_pred = model_instance.predict(X_val)
    if class_name == 'LinearRegression':
        return {
            'mean_absolute_error': metrics.mean_absolute_error(y_val, y_pred),
            'mean_squared_error': metrics.mean_squared_error(y_val, y_pred),
            'root_mean_squared_error': metrics.mean_squared_error(y_val, y_pred, squared = False)
        }
    elif class_name in ['LogisticRegression', 'GradientBoostingClassifier']:
        tn, fp, fn, tp = metrics.confusion_matrix(y_val, y_pred).ravel()
        return {
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'true_positives': int(tp)
        }
    else:
        return {}

def get_other_attribs(class_name, model_instance):
    """
    Return post-fit attributes of each model type as appropriate
    Expects class name and actual model instance
    """
    if class_name == 'LinearRegression':
        return {
            'intercept': model_instance.intercept_,
            'coefficients': list(zip(model_instance.feature_names_in_, model_instance.coef_.tolist()))
        }
    elif class_name == 'LogisticRegression':
        return {
            'class_labels': model_instance.classes_.tolist(),
            'intercept': model_instance.intercept_.tolist(),
            'coefficients': list(zip(model_instance.feature_names_in_, model_instance.coef_.tolist()))
        }
    elif class_name == 'GradientBoostingClassifier':
        return {
            'feature_importances': model_instance.feature_importances_.tolist()
        }
    else:
        return {}