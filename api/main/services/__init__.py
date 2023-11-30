import os

from api.main.services.stock_service import AlphaVantageService, StockService
from ..models.responses.stocks import AnalyticsResponse

provider = os.getenv("SYMBOLS_PROVIDER") or ""

analytics_catalog = [
    AnalyticsResponse(id="SMA", algorithm="simple moving average"),
    AnalyticsResponse(id="EMA", algorithm="xponential moving average"),
    AnalyticsResponse(id="RSI", algorithm="relative strength index"),
    AnalyticsResponse(id="ADA", algorithm="Advanced Analytics"),
]

stock_provider:StockService=None

if provider == "alpha_vantage":
    stock_provider = AlphaVantageService(
        uri=os.getenv("SYMBOLS_URL"),
        api_key=os.getenv("SYMBOLS_KEY"),
        api_secret=os.getenv("SYMBOLS_SECRET"),
    )
else:
    stock_provider = StockService()
