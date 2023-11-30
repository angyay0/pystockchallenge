import jwt

from flask import request, jsonify, make_response
from functools import wraps
from api.main.models.user_model import User
from api.main.models.responses.user import UserResponse
from api.main.services.auth_service import TOKEN_SALT


# decorator for verifying the JWT with scope parameter
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "authorization" in request.headers and request.headers[
            "authorization"
        ].startswith("Bearer"):
            token = request.headers["authorization"].replace("Bearer ", "")
        # return 401 if token is not passed
        if not token:
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, TOKEN_SALT, algorithms=["HS512"])
            current_user = User.query.filter_by(id=data["sub"]).first()
        except:
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        # returns the current logged in users context to the routes
        return f(UserResponse(current_user.id, current_user.user), *args, **kwargs)

    return decorator
