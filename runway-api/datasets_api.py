from flask import Blueprint, jsonify, session, request
from flask_cors import CORS
from app import app_db
from models.dataset import Dataset, Datafile
from sqlalchemy import or_
from auth_api import requires_auth
from json import loads, dumps
import pandas as pd
from io import StringIO

datasets_api = Blueprint("datasets_api", __name__)

@datasets_api.route("/", methods = ["GET"])
def list_datasets():
    user = session.get("user")
    if user is None:
        return [dataset.serialize() for dataset in app_db.session.query(Dataset).filter(Dataset.is_public.is_(True)).all()], 200, {'Content-Type':'application/json'} 
    else:
        return [dataset.serialize() for dataset in app_db.session.query(Dataset).filter(or_(Dataset.is_public.is_(True), Dataset.created_by == user)).all()], 200, {'Content-Type':'application/json'} 

@datasets_api.route("/<id>", methods = ["GET"])
def get_dataset_detail(id):
    result = app_db.session.get(Dataset, id)
    return dumps(result.serialize()), 200, {'Content-Type':'application/json'} 

@datasets_api.route("/", methods = ["POST"])
@requires_auth
def create_dataset():
    ds_dict = loads(request.data)
    ds_dict.pop("id", None)
    ds = Dataset(**ds_dict)
    app_db.session.add(ds)
    app_db.session.commit()
    return dumps({'success': True, 'new_dataset_id': ds.id}), 200, {'Content-Type':'application/json'}

@datasets_api.route("/<id>", methods = ["DELETE"])
@requires_auth
def delete_dataset(id):
    ds = app_db.session.get(Dataset, id)
    app_db.session.delete(ds)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@datasets_api.route("sharing/<id>/<is_public>", methods = ["POST"])
@requires_auth
def set_sharing(id, is_public):
    ds = app_db.session.get(Dataset, id)
    ds.is_public = True if is_public == "true" else False
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@datasets_api.route("/analyze/<id>", methods = ["GET"])
def analyze_dataset(id):
    analysis = { }
    ds = app_db.session.get(Dataset, id)
    for file in ds.files:
        file_analysis = { }
        if file.content_type == "text/csv":
            df = pd.read_csv(StringIO(file.content.decode()))
            file_analysis['nulls'] = df.isnull().sum().to_dict()
            file_analysis['columns'] = [{ 'name': name, 'dtype': str(dtype) } for name, dtype in df.dtypes.items()]
        analysis[file.name] = file_analysis

    return dumps(analysis), 200, {'Content-Type':'application/json'}

@datasets_api.route("/datafiles/<datafile_id>", methods = ["GET"])
@requires_auth
def download_file(datafile_id):
    df = app_db.session.get(Datafile, datafile_id)
    return df.content, 200, {'Content-Type': df.content_type}

@datasets_api.route("/datafiles/<created_by>/<dataset_id>", methods = ["POST"])
@requires_auth
def upload_files(created_by, dataset_id):
    if 'file' not in request.files:
        return "No file element present", 400
    file = request.files['file']
    if file.filename == '':
        return "No files selected", 400
    df = Datafile(dataset_id = dataset_id, name = file.filename, content_type = file.content_type, content = file.read(), created_by = created_by)
    app_db.session.add(df)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@datasets_api.route("/datafiles/<datafile_id>", methods = ["DELETE"])
@requires_auth
def delete_file(datafile_id):
    df = app_db.session.get(Datafile, datafile_id)
    app_db.session.delete(df)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}
