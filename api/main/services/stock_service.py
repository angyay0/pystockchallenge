from datetime import datetime
import requests

class StockService:
    uri: str
    name: str

    def get_stock_data(self, analytic, interval='daily', serie_type="close", period=10, save=False, extra_param=None):
        return {}


class AlphaVantageService(StockService):
    key: str
    secret: str

    def __init__(self, uri, api_key, api_secret):
        self.name = "ALPHA VANTAGE"
        self.uri = uri
        self.key = api_key
        self.secret = api_secret

    def get_stock_data(self, analytic, interval='daily', serie_type="close", period=10, save=False, extra_param=None):
        url = '{}/query?function={}&symbol={}&interval={}&time_period={}&series_type={}&&apikey={}' \
            .format(
                self.uri,
                analytic.analytics,
                analytic.Portfolio.StockSymbol.symbol,
                interval,
                period,
                serie_type,
                self.key
            )
        if extra_param:
            url = '{}{}'.format(url, extra_param)
        
        request_response = requests.get(url)
        data = request_response.json()

        return {
            'url': url,
            'data': data
        }
