from flask import Blueprint, jsonify
from flask_cors import CORS
from auth import requires_auth

test_api = Blueprint('test_api', __name__)
CORS(test_api, expose_headers=["Content-Type", "Authorization"], origins=['http://localhost:5173'])

@test_api.route("/private")
@requires_auth
def private():
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)
