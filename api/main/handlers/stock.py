import re
import datetime

from .database import save_changes, delete
from api.main.models.stock_models import *
from api.main.models.responses.api_response import APIResponse, APIResponsePaged
from api.main.utils.dto import stocks_to_response, stocks_portfolio_to_response
from api.main.utils.args_validator import are_stocks_args_valid
from api.main.utils.args_validator import are_portfolio_args_valid

NUMERIC_REGEX = "^[0-9]+$"


def get_market_symbols(args):
    page = 0
    stocks_raw = StockSymbols.query.all()
    total = len(stocks_raw)
    response = None

    if args != {} and are_stocks_args_valid(args):
        page = __convertion__(NUMERIC_REGEX, args.get("page", "1"), 1, int)
        size = __convertion__(NUMERIC_REGEX, args.get("size", "10"), 10, int)
        total = int(total / size)
        prev = 1 if page == 1 else page - 1
        nxt = (page + 1) if page < total else page
        stocks_raw = StockSymbols.query.paginate(page, size, False).items
        response = APIResponsePaged(
            code=0,
            message="Sucess",
            page=page,
            prev="?size={}&page={}".format(size, prev),
            next="?size={}&page={}".format(size, nxt),
            data=stocks_to_response(stocks_raw) if len(stocks_raw) > 0 else [],
        )
    else:
        response = APIResponsePaged(
            code=0,
            message="Sucess",
            page=1,
            prev="",
            next="",
            data=stocks_to_response(stocks_raw) if len(stocks_raw) > 0 else [],
        )

    return response


def get_user_stock_portfolio(user, args):
    response = None
    portfolio_raw = UserStockPortfolio.query.filter_by(user_id=user.id).all()
    stocks_ids = [x.id for x in portfolio_raw]
    analytics_raw = UserPortfolioAnalytics.query.filter(
        UserPortfolioAnalytics.id.in_(stocks_ids)
    ).all()
    total = len(portfolio_raw)

    if are_portfolio_args_valid(args):
        page = __convertion__(NUMERIC_REGEX, args.get("page", "1"), 1, int)
        size = __convertion__(NUMERIC_REGEX, args.get("size", "10"), 10, int)
        active = bool(args.get("active", "True"))
        total = int(total / size)
        prev = 1 if page == 1 else page - 1
        nxt = (page + 1) if page < total else page
        portfolio_raw = (
            UserStockPortfolio.query.filter_by(user_id=user.id, active=active)
            .paginate(page, size)
            .items
        )
        stocks_ids = [x.id for x in portfolio_raw]
        analytics_raw = UserPortfolioAnalytics.query.filter(
            UserPortfolioAnalytics.id.in_(stocks_ids)
        ).all()
        response = APIResponsePaged(
            code=0,
            message="Sucess",
            page=page,
            prev="?size={}&page={}".format(size, prev),
            next="?size={}&page={}".format(size, nxt),
            data=(
                stocks_portfolio_to_response(portfolio_raw, analytics_raw)
                if len(portfolio_raw) > 0
                else []
            ),
        )
    else:
        response = APIResponsePaged(
            code=0,
            message="Sucess",
            page=1,
            prev="",
            next="",
            data=(
                stocks_portfolio_to_response(portfolio_raw, analytics_raw)
                if len(portfolio_raw) > 0
                else []
            ),
        )

    return response


def save_user_stock_portfolio(user, payload):
    response = None
    symbol = StockSymbols.query.filter_by(symbol=payload["symbol"]).first()
    if symbol:
        symbolPorfolio = UserStockPortfolio.query.filter_by(
            user_id=user.id, symbol_id=symbol.id
        ).first()
        if not symbolPorfolio:
            symbolPorfolio = UserStockPortfolio(
                user_id=user.id,
                symbol_id=symbol.id,
                active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            save_changes(symbolPorfolio)

            response = APIResponse(code=0, message="Sucess", data=True)
        else:
            response = APIResponse(code=2, message="Already in Portfolio", data=False)

            if not symbolPorfolio.active:
                symbolPorfolio.active = True
                save_changes(symbolPorfolio)
                response.data = True
    else:
        response = APIResponse(code=-1, message="Symbol is not tracked", data=False)

    return response


def soft_delete_from_portfolio(user, payload):
    response = None
    symbolPorfolio = (
        UserStockPortfolio.query.join(StockSymbols)
        .filter(
            UserStockPortfolio.user_id == user.id,
            StockSymbols.symbol == payload["symbol"],
        )
        .first()
    )
    if symbolPorfolio:
        if symbolPorfolio.active:
            symbolPorfolio.active = False
            save_changes(symbolPorfolio)
        response = APIResponse(code=0, message="Sucess", data=True)
    else:
        response = APIResponse(code=-1, message="Symbol is not tracked", data=False)

    return response


def __convertion__(regex, string, default, type):
    if re.search(regex, string):
        return type(string)
    else:
        return default
