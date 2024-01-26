import time
from pybit.unified_trading import HTTP
def current_price(coin):
    session = HTTP()
    return float(session.get_tickers(
        category="inverse",
        symbol=coin,
    )['result']['list'][0]['lastPrice'])
print(current_price("SOLUSDT"))
