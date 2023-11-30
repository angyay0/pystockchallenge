import os
import unittest
import csv
import requests
import datetime

from dotenv import load_dotenv
from logging import debug
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api import blueprint
from api.main import create_app, db
from api.main.utils.encryption import hash_salt
from api.main.models.user_model import User
from api.main.models.stock_models import StockSymbols

port = os.getenv("PORT") or 5001
api = create_app(os.getenv("ENV") or "dev")
api.register_blueprint(blueprint)

api.app_context().push()

manager = Manager(api)

migrate = Migrate(api, db)

manager.add_command("db", MigrateCommand)


@manager.command
def run():
    api.run(port=port)


@manager.command
def docker_run():
    api.run(debug=False, host="0.0.0.0", port=port)


@manager.command
def test():
    """Runs the unit tests."""
    load_dotenv()
    tests = unittest.TestLoader().discover("api/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def seed_user():
    """Runs Initial Data load from provider"""
    db.session.add(
        User(
            user="test@mail.com",
            password=hash_salt("Testing1"),
            otp_active=False,
            active=True,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
    )
    db.session.commit()
    print("== SEED USER MIGRATED ==")


@manager.command
def symbols_alpha():
    """Runs Initial Data load from provider"""
    SYMBOLS_URL = os.getenv("SYMBOLS_URL") or ""
    SYMBOLS_PROVIDER = os.getenv("SYMBOLS_PROVIDER") or ""
    SYMBOLS_URL += "query?function=LISTING_STATUS&apikey=demo"

    with requests.Session() as session:
        tmp = session.get(SYMBOLS_URL)
        tmp_decoded = tmp.content.decode("UTF-8")
        symbols = list(csv.reader(tmp_decoded.splitlines(), delimiter=","))
        symbols.pop(0)
        [
            db.session.add(StockSymbols.from_provider(SYMBOLS_PROVIDER, symbol))
            for symbol in symbols
        ]
        db.session.commit()
        print("== ALPHA VANTAGE SYMBOLS MIGRATED ==")


if __name__ == "__main__":
    manager.run()
