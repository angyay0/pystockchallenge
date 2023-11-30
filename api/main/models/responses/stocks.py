from .base import BaseResponse


class StockSymbolResponse(BaseResponse):
    symbol: str
    description: str

    def __init__(self, symbol, description):
        self.symbol = symbol
        self.description = description

    def serialize(self):
        return {"symbol": self.symbol, "description": self.description}


class AnalyticsResponse(BaseResponse):
    id: int
    algorithm: str

    def __init__(self, algorithm, id):
        self.algorithm = algorithm
        self.id = id

    def serialize(self):
        return {"algorithm": self.algorithm, "id": self.id}


class AnalyticsDataResponse(BaseResponse):
    algorithm: str
    period: str
    data: {}

    def __init__(self, algorithm, symbol, data):
        self.algorithm = algorithm
        self.symbol = symbol
        self.data = data

    def serialize(self):
        return {"algorithm": self.algorithm, "period": self.period, "data": self.data}


class StockPortfolioResponse(BaseResponse):
    analytics: []
    symbol: StockSymbolResponse
    active: bool

    def __init__(self, symbol, active, analytics):
        self.symbol = symbol
        self.active = active
        self.analytics = analytics

    def serialize(self):
        return {
            "symbols": self.symbol.serialize(),
            "analytics": [x.serialize() for x in self.analytics],
            "active": self.active,
        }
