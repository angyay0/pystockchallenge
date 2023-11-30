from api.test.test_utils import get_random_string


def sigup_payload():
    return {
        "email": "tester{}@test.com".format(get_random_string(8)),
        "password": "Testing1",
        "name": "Test",
        "last_name": "Test",
        "phone_number": "1234123456",
        "otp": False
    }