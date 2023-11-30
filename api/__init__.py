import os
from pydoc import doc
from flask_restplus import Api
from flask import Blueprint

from .main.controllers.health import health_api as health_ns
from .main.controllers.auth import auth_api as auth_ns
from .main.controllers.stock import stock_api as stock_ns

run_env = os.getenv("ENV") or "dev"
show_doc = "/doc" if run_env == "dev" else False
blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="API",
    version="1.0.0",
    description="Stock Take Home API",
    doc=show_doc,
)

if run_env == "dev":
    api.add_namespace(health_ns, path="/health")

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(stock_ns, path="/stocks")
