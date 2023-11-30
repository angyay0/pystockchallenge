from api.main.models.stock_models import *
from api.main.models.responses.stocks import *


def stock_to_response(stock):
    return StockSymbolResponse(stock.symbol, stock.description)


def analytics_to_response(analytic):
    return AnalyticsResponse(analytic.analytics, analytic.id)


def portfolio_to_response(portfolio, analytics):
    return StockPortfolioResponse(
        stock_to_response(portfolio.StockSymbol), portfolio.active, analytics
    )


def stocks_to_response(stocks):
    data = []
    for stock in stocks:
        data.append(stock_to_response(stock))
    return data


def stocks_portfolio_to_response(portfolio, analytics):
    data = []
    for item in portfolio:
        item_analytics = get_analytics_filtered(item.id, analytics)
        data.append(portfolio_to_response(item, item_analytics))
    return data


def get_analytics_filtered(id, analytics):
    data = []
    for a in analytics:
        if a.id == id:
            data.append(analytics_to_response(a))
    return data
