from api.test.test_utils import get_random_string


def sigup_payload():
    return {
        "email": "tester{}@test.com".format(get_random_string(8)),
        "password": "Testing1",
        "name": "Test",
        "last_name": "Test",
        "phone_number": "1234123456",
        "otp": False,
    }


def login_payload():
    return {"email": "test@mail.com", "password": "Testing1"}


def auth_signup_payload(otp=False, rand=""):
    return {
        "email": "tester{}@test.com".format(rand),
        "password": "Testing1",
        "name": "Test",
        "last_name": "Test",
        "phone_number": "1234123456",
        "otp": otp,
    }


def expired_token():
    return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOjEsImlhdCI6MTcwMTI0NDgwMiwiZXhwIjoxNzAxMjUyMDAyfQ.2fhonRGAsmI8pmfcBkUEBrAAuaGPxC2W5UpHm8H-vtb_PqD-g2UrLFlFaGms2aERL0esdnD4f2WUU7YOeFmNLw"
