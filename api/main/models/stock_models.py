from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

from .. import db


class StockSymbols(db.Model):
    __tablename__ = "StockSymbols"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    symbol = db.Column(db.String(30), unique=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    provider = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    portfolios = db.relationship("UserStockPortfolio", backref="StockSymbol", lazy=True)

    def from_provider(provider, provider_symbol):
        return StockSymbols(
            symbol=provider_symbol[0],
            type="{},{}".format(provider_symbol[2], provider_symbol[3]),
            description=provider_symbol[1],
            provider=provider,
            active=True if provider_symbol[6] == "Active" else False,
            created_at=datetime.strptime(provider_symbol[4], "%Y-%m-%d"),
            updated_at=datetime.utcnow(),
        )

    def __repr__(self) -> str:
        return "<Stock Symbol'{}'".format(self.symbol)


class SymbolRequests(db.Model):
    _tablename__ = "StockSymbolRequest"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    provider = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String, nullable=False)
    response = db.Column(JSONB, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return "<Symbol Requests'{}'".format(self.id)


class UserStockPortfolio(db.Model):
    __tablename__ = "UserStockPortfolio"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    symbol_id = db.Column(
        db.BigInteger, db.ForeignKey("StockSymbols.id"), nullable=False
    )
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    analytics = db.relationship("UserPortfolioAnalytics", backref="Portfolio", lazy=True)

    def __repr__(self) -> str:
        return "<User Stock Portfolio'{}'".format(self.symbol)


class UserPortfolioAnalytics(db.Model):
    __tablename__ = "UserPortfolioAnalytics"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    portfolio_id = db.Column(
        db.BigInteger, db.ForeignKey("UserStockPortfolio.id"), nullable=False
    )
    analytics = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return "<User Portfolio Analytics'{}'".format(self.symbol)
