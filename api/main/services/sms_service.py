import os
from unittest import result
from .. import sns

from flask import current_app

TEMPLATE_SMS = "Your SignIn code is: @code. It expires in 5 minutes."


def send_sms(code, number):
    if current_app.config["TESTING"]:
        os.environ["OTP_TESTING_CODE"] = "{}".format(code)
    else:
        try:
            results = sns.publish(
                PhoneNumber=number, Message=TEMPLATE_SMS.replace("@code", code)
            )
            (
                print("SMS Sent")
                if results and results["MessageId"]
                else print("SMS Failed")
            )
        except:
            print("SMS Failed")
