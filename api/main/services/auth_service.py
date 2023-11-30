import secrets
import string
import jwt
from datetime import datetime, timedelta
from api.main.utils import protected_apis

SALT = "das893&&5==!kdvnkel%$322356///343"
TOKEN_SALT = "jhkasdjha&eka57829/(8asdjF%)=="


def generate_code(length=6):
    code = ""
    while code == "":
        code = "".join(secrets.choice(string.digits) for x in range(length))

    return code


def generate_otp_token(code_id, iat, expiry):
    return jwt.encode(
        payload={"sub": code_id, "iat": iat, "exp": expiry, "scope": protected_apis},
        key=SALT,
        algorithm="HS512",
    )


def generate_scoped_session(user_id):
    return jwt.encode(
        payload={
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=2),
        },
        key=TOKEN_SALT,
        algorithm="HS512",
    )


def get_otp_id(token):
    try:
        payload = jwt.decode(token, SALT, algorithms=["HS512"])
        return int(payload["sub"])
    except Exception:
        print("Error with Token")

    return 0
