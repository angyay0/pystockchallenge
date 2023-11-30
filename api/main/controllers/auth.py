from flask import request, make_response, jsonify
from flask_restplus import Resource
from api.main.models.responses.api_response import APIResponse

from api.main.utils.definitions import AuthDefinition

from api.main.handlers.auth import (
    sign_in,
    sign_up,
    otp_sign_in,
    update_user,
    soft_delete_user,
)
from api.main.utils.token_required import token_required

auth_api = AuthDefinition.api
_userDto = AuthDefinition.user
_otpDto = AuthDefinition.otp
_signInDto = AuthDefinition.signIn
_updateUserDto = AuthDefinition.userUpdate


@auth_api.route("/user")
@auth_api.response(200, "Success")
@auth_api.response(400, "Error")
class SignIn(Resource):
    @auth_api.doc("SignIn user")
    @auth_api.expect(_signInDto, validate=True)
    def post(self):
        data = request.json
        if data:
            result = sign_in(data)
            if result:
                return result.serialize()

        auth_api.response(400, "Error")
        return None

    @auth_api.doc("SignUp user")
    @auth_api.expect(_userDto, validate=True)
    def put(self):
        result = APIResponse(-1, "", None)
        data = request.json
        code = 200
        if data:
            result = sign_up(data)

        if result:
            if result.code != 0:
                code = 400

        return make_response(jsonify(result.serialize()), code)

    @auth_api.response(401, "Unauthorized")
    @auth_api.doc("Update User")
    @auth_api.expect(_updateUserDto, validate=True)
    @token_required
    def patch(user, self):
        data = request.json
        if data:
            result = update_user(user, data)
            code = 200
            if result:
                if result.data.message == "CannotUpdate":
                    code = 400
                return make_response(jsonify(result.serialize()), code)

        auth_api.response(400, "Error")
        return None

    @auth_api.response(401, "Unauthorized")
    @auth_api.doc("Deactivate User")
    @token_required
    def delete(user, self):
        result = soft_delete_user(user)
        code = 200
        if result.code != 0:
            code = 400

        return make_response(jsonify(result.serialize()), code)


@auth_api.route("/user/tfa")
class OTPValidate(Resource):
    @auth_api.response(200, "Success")
    @auth_api.doc("OTP execute")
    @auth_api.expect(_otpDto, validate=True)
    def post(self):
        data = request.json
        status = 200
        if data:
            result = otp_sign_in(data)
            if result:
                if hasattr(result.data, "message"):
                    status = 400
                return make_response(jsonify(result.serialize()), status)

        return make_response("", 400)
