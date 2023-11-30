from concurrent.futures import ThreadPoolExecutor
import os
import datetime

from .database import save_changes, delete
from api.main.services import analytics_catalog, stock_provider
from api.main.models.stock_models import *
from api.main.models.responses.api_response import APIResponse, APIResponsePaged
from api.main.models.responses.stocks import AnalyticsResponse, AnalyticsDataResponse
from api.main.utils.dto import stocks_to_response, stocks_portfolio_to_response

provider = os.getenv('SYMBOLS_PROVIDER') or 'N/A'

def get_analytics():
    response = APIResponsePaged(
        code=0, message="Success", page=1, next="", prev="", data=analytics_catalog
    )
    return response


def save_analytic(user, payload):
    response = None
    symbol = (
        UserStockPortfolio.query.join(StockSymbols)
        .filter(
            UserStockPortfolio.user_id == user.id,
            StockSymbols.symbol == payload["symbol"],
        )
        .first()
    )
    if symbol:
        analytics = UserPortfolioAnalytics.query.filter_by(
            portfolio_id=symbol.id, analytics=payload["analytic"]
        ).first()
        if not analytics:
            analytics = UserPortfolioAnalytics(
                portfolio_id=symbol.id,
                analytics=payload["analytic"],
                active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            save_changes(analytics)
            response = APIResponse(
                code=0, message="Analytics for stock added", data=True
            )
        elif not analytics.active:
            analytics.active = True
            save_changes(analytics)
            response = APIResponse(code=0, message="Analytics Re activated", data=True)
        else:
            response = APIResponse(code=-1, message="Analytics not added", data=False)
    else:
        response = APIResponse(code=-1, message="Symbol is not tracked", data=False)

    return response


def delete_analytics(user, payload):
    response = None
    analytics = UserPortfolioAnalytics.query.filter_by(id=payload["id"]).first()
    if analytics and analytics.active:
        analytics.active = False
        delete(analytics)
        response = APIResponse(code=0, message="Analytics for stock removed", data=True)
    else:
        response = APIResponse(code=-1, message="Analytics already removed", data=False)

    return response

def process(analytic, params):
    
    return stock_provider.get_stock_data(
        analytic=analytic,
        interval=params['interval'],
        serie_type=params['type'],
        save=params['save'],
        period=params['period'] if params['period'] < 1 else 10
    )

def process_analytics(user, data):
    response = APIResponse(code=-1,message='Error',data=None)
    ids = data["ids"] or []
    if len(ids) > 0:
        collected = []
        analytics = UserPortfolioAnalytics.query.filter(
            UserPortfolioAnalytics.id.in_(ids)
        ).all()

        with ThreadPoolExecutor(max_workers=len(ids)) as pool:
            for analytic in analytics:
                analytic_result = pool.submit(process, analytic, data).result()
                collected.append(analytic_result['data'])
                if data['save']:
                    binnacle= SymbolRequests(
                        user_id=analytic.Portfolio.user_id,
                        provider=provider,
                        url=analytic_result['url'],
                        response=analytic_result['data'],
                        created_at=datetime.utcnow()
                    )
                    save_changes(binnacle)


        
        response=APIResponse(
            code=0,
            message='Success',
            data=collected
        )

    return response
