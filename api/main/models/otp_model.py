from .. import db


class OTPModel(db.Model):
    __tablename__ = "OTPCodes"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    code = db.Column(db.String(6), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return "<OTP Code '{}'".format(self.id)
