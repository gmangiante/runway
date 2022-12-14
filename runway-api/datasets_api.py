from flask import Blueprint, jsonify, session, request
from flask_cors import CORS
from app import app_db
from models.dataset import Dataset, Datafile
from sqlalchemy import or_
from auth_api import requires_auth
from json import loads, dumps
import pandas as pd
from io import StringIO
import base64
from models.visualizations import DatasetVisualization

datasets_api = Blueprint("datasets_api", __name__)

@datasets_api.route("/", methods = ["GET"])
def list_datasets():
    """
    list all datasets available to this user (or only public if anonymous)
    """
    user = session.get("user")
    if user is None:
        return [dataset.serialize() for dataset in app_db.session.query(Dataset).filter(Dataset.is_public.is_(True)).all()], 200, {'Content-Type':'application/json'} 
    else:
        return [dataset.serialize() for dataset in app_db.session.query(Dataset).filter(or_(Dataset.is_public.is_(True), Dataset.created_by == user)).all()], 200, {'Content-Type':'application/json'} 

@datasets_api.route("/<id>", methods = ["GET"])
def get_dataset_detail(id):
    """
    Get details on single dataset
    """
    result = app_db.session.get(Dataset, id)
    return dumps(result.serialize()), 200, {'Content-Type':'application/json'} 

@datasets_api.route("/", methods = ["POST"])
@requires_auth
def create_dataset():
    """
    Create a dataset from JSON request (auth required)
    """
    ds_dict = loads(request.data)
    ds_dict.pop("id", None)
    ds = Dataset(**ds_dict)
    app_db.session.add(ds)
    app_db.session.commit()
    return dumps({'success': True, 'new_dataset_id': ds.id}), 200, {'Content-Type':'application/json'}

@datasets_api.route("/<id>", methods = ["DELETE"])
@requires_auth
def delete_dataset(id):
    """
    Delete a dataset from ID parameter (auth required)
    """
    ds = app_db.session.get(Dataset, id)
    app_db.session.delete(ds)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@datasets_api.route("sharing/<id>/<is_public>", methods = ["POST"])
@requires_auth
def set_sharing(id, is_public):
    """
    Change dataset sharing from public-private or vice-versa (auth required)
    """
    ds = app_db.session.get(Dataset, id)
    ds.is_public = True if is_public == "true" else False
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@datasets_api.route("/analyze/<id>", methods = ["GET"])
def analyze_dataset(id):
    """
    Return useful information about an existing dataset, based on ID
    Includes nulls, data types, unique value counts, distributions per-column, and correlation data
    """
    analysis = { }
    ds = app_db.session.get(Dataset, id)
    for file in ds.files:
        file_analysis = {'dataset_id': id, 'datafile_id': file.id, 'datafile_name': file.name }
        if file.content_type == "text/csv":
            df = pd.read_csv(StringIO(file.content.decode()))
            file_analysis['nulls'] = df.isnull().sum().to_dict()
            file_analysis['columns'] = [{ 'name': name, 'dtype': str(dtype) } for name, dtype in df.dtypes.items()]
            file_analysis['unique'] = [ {'column': col, 'unique_val_count': df[col].nunique() } for col in df.columns ]
            file_analysis['distributions'] = [ {'column': col, 'distribution': [ {'value': str(val), 'occurrences': occ}
                for val, occ in df[col].value_counts().items()]} for col in df.columns ]
            corr = df.corr()
            file_analysis['corr'] = [{ 'column1': col, 'column2': othercol, 'corr_val': corr.loc[col, othercol] } for col in corr.index for othercol in corr.index]
        analysis[file.name] = file_analysis
    return dumps(analysis), 200, {'Content-Type':'application/json'}

@datasets_api.route("/datafiles/<datafile_id>", methods = ["GET"])
@requires_auth
def download_file(datafile_id):
    """
    Download an existing datafile by ID (auth required)
    """
    df = app_db.session.get(Datafile, datafile_id)
    return df.content, 200, {'Content-Type': df.content_type}

@datasets_api.route("/datafiles/<created_by>/<dataset_id>", methods = ["POST"])
@requires_auth
def upload_files(created_by, dataset_id):
    """
    Upload a datafile to an existing dataset (auth required)
    """
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
    """
    Delete a datafile from a dataset by ID (auth required)
    """
    df = app_db.session.get(Datafile, datafile_id)
    app_db.session.delete(df)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}

@datasets_api.route("/datafiles/<datafile_id>/transform/dropnulls", methods = ["POST"])
@requires_auth
def drop_nulls(datafile_id):
    """
    Transform - drop nulls from datafile by ID (auth required)
    Expects axis (rows or columns) and list of columns to consider
    """
    requestData = loads(request.data)
    file = app_db.session.get(Datafile, datafile_id)
    df = pd.read_csv(StringIO(file.content.decode()))
    df = df.dropna(axis = requestData['axis'], subset = requestData['columns'])
    return_id = save_file_for_xform(file, df, 'dropnulls', requestData['duplicate'])
    return dumps({'success':True, 'datafile_id': return_id}), 200, {'Content-Type':'application/json'}

@datasets_api.route("/datafiles/<datafile_id>/transform/imputenulls", methods = ["POST"])
@requires_auth
def impute_nulls(datafile_id):
    """
    Transform - Impute nulls per-column - can impute zero, mean, mode, or median  (auth required)
    Expects impute mode and list of columns
    """
    requestData = loads(request.data)
    file = app_db.session.get(Datafile, datafile_id)
    df = pd.read_csv(StringIO(file.content.decode()))
    impute_mode = requestData['impute']
    for col in requestData['columns']:
        if impute_mode == 'zero':
            df.loc[df[col].isnull(), col] = 0
        elif impute_mode == 'emptystring':
            df.loc[df[col].isnull(), col] = ''
        elif impute_mode == 'mean':
            mean = df[col].mean()
            df.loc[df[col].isnull(), col] = mean
        elif impute_mode == "mode":
            mode = df[col].mode()
            df.loc[df[col].isnull(), col] = mode
        elif impute_mode == "median":
            median = df[col].median()
            df.loc[df[col].isnull(), col] = median
    return_id = save_file_for_xform(file, df, 'imputenulls', requestData['duplicate'])
    return dumps({'success':True, 'datafile_id': return_id}), 200, {'Content-Type':'application/json'}

@datasets_api.route("/datafiles/<datafile_id>/transform/onehotencode", methods = ["POST"])
@requires_auth
def one_hot_encode(datafile_id):
    """
    Transform - one-hot encode columns using pd.get_dummies  (auth required)
    Expects list of columns to encode and dropFirst
    """
    requestData = loads(request.data)
    file = app_db.session.get(Datafile, datafile_id)
    df = pd.read_csv(StringIO(file.content.decode()))
    df = pd.get_dummies(df, columns = requestData['columns'], drop_first=requestData['dropFirst'])
    return_id = save_file_for_xform(file, df, 'onehotencode', requestData['duplicate'])
    return dumps({'success':True, 'datafile_id': return_id}), 200, {'Content-Type':'application/json'}

def save_file_for_xform(datafile, dataframe, xform, duplicate):
    """
    Utility function used by all transforms to either duplicate or replace transformed file
    Expects datafile (original Datafile), dataframe (transformed Dataframe), xform (name of transform), duplicate (boolean)
    """
    new_file_content = StringIO()
    dataframe.to_csv(new_file_content, index = False)
    if (duplicate):
        new_file = Datafile(dataset_id = datafile.dataset_id, name = datafile.name + f'_{xform}.csv', content_type = "text/csv", content = bytes(new_file_content.getvalue(), 'utf-8'), created_by = datafile.created_by)
        app_db.session.add(new_file)
        app_db.session.commit()
        return_id = new_file.id
    else:
        datafile.content = bytes(new_file_content.getvalue(), 'utf-8')
        app_db.session.commit()
        return_id = datafile.id
    return return_id

@datasets_api.route("/visualizations/<dataset_id>", methods = ["POST"])
@requires_auth
def uploadVisualization(dataset_id):
    """
    TODO - future capability
    Upload visualization of dataset to database
    Expects request body to be base64-encoded PNG created by toDataURL()
    """
    imageData64 = request.data[len("data:image/png;base64,"):]
    imageData = base64.decodebytes(imageData64)
    viz = DatasetVisualization(dataset_id = dataset_id, name = "test", is_public = True, content_type = "image/png",
        content = imageData, created_by = "gabrielmangiante@gmail.com" )
    app_db.session.add(viz)
    app_db.session.commit()
    return dumps({'success':True}), 200, {'Content-Type':'application/json'}