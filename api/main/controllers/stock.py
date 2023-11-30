from flask import request, jsonify, make_response
from flask_restplus import Resource

from api.main.utils.definitions import StocksDefinition
from api.main.handlers.analytics import (
    get_analytics,
    save_analytic,
    delete_analytics,
    process_analytics,
)
from api.main.handlers.stock import (
    get_market_symbols,
    save_user_stock_portfolio,
    get_user_stock_portfolio,
    soft_delete_from_portfolio,
)
from api.main.utils.token_required import token_required

stock_api = StocksDefinition.api
stockPortfolio = StocksDefinition.stockPortfolio
analyticsSymbol = StocksDefinition.analyticsSymbol
analyzePortfolio = StocksDefinition.analyzePortfolio


@stock_api.route("/")
@stock_api.response(200, "Success")
@stock_api.response(400, "Bad Request")
@stock_api.response(401, "Unauthorized")
@stock_api.response(403, "Unauthorized")
class StockAPI(Resource):
    @stock_api.doc("Get Market Symbols")
    @token_required
    def get(user, self):
        args = dict(request.args)
        data = get_market_symbols(args)
        code = 200
        if data and data.code != 0:
            code = 400

        return make_response(jsonify(data.serialize()), code)


@stock_api.route("/portfolio")
@stock_api.response(200, "Success")
@stock_api.response(400, "Bad Request")
@stock_api.response(401, "Unauthorized")
@stock_api.response(403, "Unauthorized")
class UserStockPortfolio(Resource):
    @stock_api.doc("Get Portfolio Symbols")
    @token_required
    def get(user, self):
        args = dict(request.args)
        data = get_user_stock_portfolio(user, args)
        code = 200
        if data and data.code != 0:
            code = 400

        return make_response(jsonify(data.serialize()), code)

    @stock_api.doc("Save/Activate Portfolio Symbols")
    @stock_api.expect(stockPortfolio, validate=True)
    @token_required
    def put(user, self):
        data = request.json
        data = save_user_stock_portfolio(user, data)
        code = 200
        if data and data.code != 0:
            code = 400

        return make_response(jsonify(data.serialize()), code)

    @stock_api.doc("Remove Symbol from Portfolio")
    @token_required
    def delete(user, self):
        data = request.json
        data = soft_delete_from_portfolio(user, data)
        code = 200
        if data and data.code != 0:
            code = 400

        return make_response(jsonify(data.serialize()), code)


@stock_api.route("/analytics")
@stock_api.response(200, "Success")
@stock_api.response(400, "Bad Request")
@stock_api.response(401, "Unauthorized")
@stock_api.response(403, "Unauthorized")
class PortfolioStockAnalytics(Resource):
    @stock_api.doc("Get Analytics Available")
    @stock_api.header("Authorization", "Bearer")
    @token_required
    def get(user, self):
        return get_analytics().serialize()

    @stock_api.doc("Get Analytics Processing")
    @stock_api.expect(analyzePortfolio, validate=True)
    @token_required
    def post(user, self):
        data = request.json
        response = process_analytics(user, data)
        code = 200
        if response and response.code != 0:
            code = 400

        return make_response(jsonify(response.serialize()), code)

    @stock_api.doc("Save/Activate Stocks Analytics")
    @stock_api.expect(analyticsSymbol, validate=True)
    @token_required
    def put(user, self):
        data = request.json
        response = save_analytic(user, data)
        code = 200
        if response and response.code != 0:
            code = 400

        return make_response(jsonify(response.serialize()), code)

    @stock_api.doc("Remove Symbol Analytics")
    @stock_api.expect(analyticsSymbol, validate=False)
    @token_required
    def delete(user, self):
        data = request.json
        data = delete_analytics(user, data)
        code = 200
        if data and data.code != 0:
            code = 400

        return make_response(jsonify(data.serialize()), code)
