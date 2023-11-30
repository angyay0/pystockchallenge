from .. import db


class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    user = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    otp_active = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return "<User '{}'".format(self.id)


class UserDetails(db.Model):
    __tablename__ = "UserDetails"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return "<UserDetails '{}'".format(self.id)
