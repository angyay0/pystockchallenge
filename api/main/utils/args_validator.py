import re

STOCKS_ARGS = ["size", "page"]
PORTFOLIO_ARGS = ["size", "active", "analytics", "page"]


def are_stocks_args_valid(args):
    keys = list(args.keys())
    valid = (
        True
        if len(keys) <= len(STOCKS_ARGS) and set(keys).issubset(set(STOCKS_ARGS))
        else False
    )
    return valid


def are_portfolio_args_valid(args):
    keys = list(args.keys())
    valid = (
        True
        if len(keys) <= len(PORTFOLIO_ARGS) and set(keys).issubset(set(PORTFOLIO_ARGS))
        else False
    )
    return valid
