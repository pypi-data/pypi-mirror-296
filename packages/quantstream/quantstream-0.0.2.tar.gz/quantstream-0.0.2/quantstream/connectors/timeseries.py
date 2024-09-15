import typing

from .url_methods import __return_json_v3, __validate_time_delta
from .urls import FMP_URLS

fmp = FMP_URLS()


def quote(
    apikey: str, symbol: typing.Union[str, list[str]]
) -> typing.Optional[list[dict]]:
    """_summary_

    Args:
        apikey (str): _description_
        symbol (typing.Union[str, typing.List[str]]): _description_

    Returns:
        typing.Optional[typing.List[typing.Dict]]: _description_
    """
    if isinstance(symbol, list):
        symbol = ",".join(symbol)
    path = f"quote/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_v3(path=path, params=query_vars)


def intraday(
    apikey: str,
    symbol: str,
    time_delta: str,
    from_date: str,
    to_date: str,
    time_series: str = fmp.default_line_param,
) -> typing.Optional[list[dict]]:
    """_summary_

    Args:
        apikey (str): _description_
        symbol (str): _description_
        time_delta (str): _description_
        from_date (str): _description_
        to_date (str): _description_
        time_series (str, optional): _description_. Defaults to fmp.default_line_param.

    Returns:
        typing.Optional[typing.List[typing.Dict]]: _description_
    """
    path = f"historical-chart/{__validate_time_delta(time_delta)}/{symbol}"
    query_vars = {"apikey": apikey}
    query_vars = {
        "apikey": apikey,
    }
    if time_series:
        query_vars["timeseries"] = time_series
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_v3(path=path, params=query_vars)


def daily(
    apikey: str,
    symbol: typing.Union[str, list],
    from_date: str = None,
    to_date: str = None,
) -> typing.Optional[list[dict]]:
    """_summary_

    Args:
        apikey (str): _description_
        symbol (typing.Union[str, typing.List]): _description_
        from_date (str, optional): _description_. Defaults to None.
        to_date (str, optional): _description_. Defaults to None.

    Returns:
        typing.Optional[typing.List[typing.Dict]]: _description_
    """
    if isinstance(symbol, list):
        symbol = ",".join(symbol)
    path = f"historical-price-full/{symbol}"
    query_vars = {
        "apikey": apikey,
    }

    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    res = __return_json_v3(path=path, params=query_vars)

    if res:
        return res.get("historicalStockList", res.get("historical", None))
    else:
        return res
