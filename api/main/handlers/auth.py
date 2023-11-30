import datetime
from datetime import timedelta

from .database import *
from api.main.models.otp_model import OTPModel
from api.main.models.user_model import User, UserDetails
from api.main.models.responses.generic import GenericResponse
from api.main.models.responses.session import SessionResponse
from api.main.models.responses.api_response import APIResponse

from api.main.services.sms_service import send_sms
from api.main.utils.encryption import hash_match, hash_salt
from api.main.services.auth_service import generate_code, generate_otp_token
from api.main.services.auth_service import get_otp_id, generate_scoped_session


def sign_up(data):
    user = User.query.filter_by(user=data["email"]).first()
    if not user:
        otp = data["otp"] if "otp" in data.keys() else False
        phone = data["phone_number"] if "phone_number" in data.keys() else None

        user = User(
            user=data["email"],
            password=hash_salt(data["password"]),
            otp_active=otp,
            active=True,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        save_changes(user)
        details = UserDetails(
            user_id=user.id,
            name=data["name"],
            last_name=data["last_name"],
            phone_number=phone,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        save_changes(details)
        return APIResponse(
            code=0,
            message="Success",
            data=GenericResponse(done=True, message="Completed"),
        )

    return APIResponse(
        code=-1,
        message="Cannot register user.",
        data=GenericResponse(done=False, message="CannotRegister"),
    )


def update_user(user_token, data):
    user = User.query.filter_by(id=user_token.id).first()
    if user:
        otp = data["otp"] if "otp" in data.keys() else False
        phone = data["phone_number"] if "phone_number" in data.keys() else None

        user.password = hash_salt(data["password"])
        user.otp_active = otp
        user.updated_at = datetime.datetime.utcnow()
        save_changes(user)

        details = UserDetails.query.filter_by(user_id=user.id).first()
        details.phone = phone
        save_changes(details)

        return APIResponse(
            code=0,
            message="Success",
            data=GenericResponse(done=True, message="Completed"),
        )

    return APIResponse(
        code=-1,
        message="Cannot register user.",
        data=GenericResponse(done=True, message="CannotRegister"),
    )


def soft_delete_user(user):
    user = User.query.filter_by(id=user.id).first()
    if user and user.active:
        user.active = False
        save_changes(user)

        return APIResponse(
            code=0,
            message="User is deactivated.",
            data=GenericResponse(done=True, message="NotActive."),
        )

    return APIResponse(
        code=-1,
        message="User is not longer active. Please request activate.",
        data=GenericResponse(done=False, message="NotActive."),
    )


def sign_in(data):
    user = User.query.filter_by(user=data["email"]).first()
    if user:
        if user.active:
            return handle_signin(user, data["password"])
        else:
            return APIResponse(
                code=-1,
                message="User is not longer active. Please request activate.",
                data=GenericResponse(done=False, message="NotActive."),
            )

    return None


def otp_sign_in(data):
    code = OTPModel.query.filter_by(id=get_otp_id(data["token"])).first()
    if code:
        if code.code == data["code"] and code.expiry >= datetime.datetime.utcnow():
            code.expiry = datetime.datetime.utcnow()
            save_changes(code)

            return APIResponse(
                code=0,
                message="Sucessful Login",
                data=SessionResponse(token=generate_scoped_session(code.user_id)),
            )
        else:
            return APIResponse(
                code=-1,
                message="Unsucessful Login",
                data=GenericResponse(done=False, message="CodeMismatch"),
            )
    else:
        return APIResponse(
            code=-1,
            message="Unsucessful Login",
            data=GenericResponse(done=False, message="ExpiredTokenOrInvalidOTP"),
        )


def handle_signin(user, pwd):
    if not user.otp_active:
        if hash_match(pwd, user.password):
            return APIResponse(
                code=0,
                message="Sucessful Login",
                data=SessionResponse(token=generate_scoped_session(user.id)),
            )
        else:
            return APIResponse(
                code=-1,
                message="Unsucessful Login",
                data=GenericResponse(done=False, message="UserOrPasswordMismatch"),
            )
    else:
        details = UserDetails.query.filter_by(user_id=user.id).first()
        code = OTPModel(
            user_id=user.id,
            code=generate_code(),
            expiry=datetime.datetime.utcnow() + timedelta(minutes=5),
        )
        save_changes(code)
        send_sms(code.code, details.phone_number)

        return APIResponse(
            code=1,
            message="Login OTP Required",
            data=SessionResponse(
                token=generate_otp_token(
                    code.id, datetime.datetime.utcnow(), code.expiry
                )
            ),
        )
