flag = int(input())
if flag == 0:
    print(1)
    import dill  # pip install dill --user

    filename = 'save.pkl'
    dill.load_session(filename)
else:
    print(0)
    from pybit.unified_trading import HTTP

    session = HTTP(api_key="fofVie6eTCqLKyFhX8", api_secret="21WRLx2EsDVJad3duK2PbzxxRdhS4P3gK2yR")
    import time as tt
    import dill
    from work_with_futures_positions import *

    clas = work_1(["A7hKrcISyhFZdzddCZ"], ["hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI"])
    leverage = 25
    coin = "MKRUSDT"
    # tks = [4, 4, 5, 6, 10]
    tks = 0.8
    mas_1 = [2, 3, 3, 3, 5, 5, 6]
    mas_2 = mas_1[::]
    buf = session.get_tickers(
        category="inverse",
        symbol=coin,
    )['result']['list'][0]['lastPrice']
    clas.add_user("fofVie6eTCqLKyFhX8", "21WRLx2EsDVJad3duK2PbzxxRdhS4P3gK2yR", coin, leverage,
                  [i * 1.2 * leverage for i in mas_1], [i * leverage for i in mas_2], 2, leverage, 60 * 60,
                  10 * leverage,
                  "marker", 5 * leverage, 15 * leverage, False, tks, {coin: float(buf)})
    ol = 0
    filename = 'save.pkl'
while True:

    ol += 1
    tt.sleep(0.5)
    buf = session.get_tickers(
        category="inverse",
        symbol=coin,
    )['result']['list'][0]['lastPrice']
    clas.obxod({coin: float(buf)})
    if ol % 100 == 0:
        print(clas.users[0].get_open_orders(float(buf)))
        print({coin: float(buf)})
        print(clas.take_price)
    if ol % 10 == 0:
        dill.dump_session(filename)
