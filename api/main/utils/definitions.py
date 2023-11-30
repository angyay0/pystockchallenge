import re
from tokenize import String
from flask_restplus import Namespace, fields


class HealthDefinition:
    api = Namespace("Health", description="Health API")


class AuthDefinition:
    api = Namespace("Auth", description="Authentication API")
    user = api.model(
        "userModel",
        {
            "email": fields.String(required=True, description="Email"),
            "password": fields.String(required=True, description="Password"),
            "name": fields.String(required=True, description="Name"),
            "last_name": fields.String(required=True, description="Lastname"),
            "phone_number": fields.String(required=False, description="Phone"),
            "otp": fields.Boolean(
                required=False, default=False, description="Enable OTP"
            ),
        },
    )
    userUpdate = api.model(
        "userUpdateModel",
        {
            "password": fields.String(required=False, description="Password"),
            "name": fields.String(required=False, description="Name"),
            "last_name": fields.String(required=False, description="Lastname"),
            "phone_number": fields.String(required=False, description="Phone"),
            "otp": fields.Boolean(
                required=False, default=False, description="Enable OTP"
            ),
        },
    )
    signIn = api.model(
        "signInModel",
        {
            "email": fields.String(required=True, description="Email"),
            "password": fields.String(required=True, description="Password"),
        },
    )
    otp = api.model(
        "otpModel",
        {
            "token": fields.String(required=True, description="Transaction Token"),
            "code": fields.String(required=True, description="OTP"),
        },
    )


class StocksDefinition:
    api = Namespace("Stocks", description="Stock Market API")
    stockPortfolio = api.model(
        "stockPortfolioModel",
        {
            "symbol": fields.String(
                required=True,
                description="The stock symbol you want to add to portfolio",
            )
        },
    )
    analyticsSymbol = api.model(
        "stockAnalyticsModel",
        {
            "id": fields.Integer(required=False, description="Analytics Symbol Id"),
            "symbol": fields.String(
                required=True,
                description="The stock symbol you want to add to portfolio",
            ),
            "analytic": fields.String(
                required=True,
                description="The stock Anaytic you want to tie to analytic",
            ),
        },
    )
    analyzePortfolio = api.model(
        "analyzeModel",
        {
            "ids": fields.List(
                fields.Integer, required=True, description="Stock Analytics Id"
            ),
            "interval": fields.String(required=True, description="Analytic interval"),
            "type": fields.String(required=True, description="Analytic serie type"),
            "period": fields.Integer(
                required=True, description="Analytics Period segment"
            ),
            "save": fields.Boolean(
                required=True, description="Wheter if save data request or not"
            ),
        },
    )
