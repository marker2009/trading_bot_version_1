import pandas as pd
from pybit.unified_trading import HTTP
import datetime
import time


def export(dataframe, name, col):  # col - измеряется в 200
    ms = datetime.datetime.now()
    un = time.mktime(ms.timetuple()) * 1000 // (1000 * 5 * 60) * (1000 * 5 * 60)
    print(un - 1000 * 12000 * dataframe)
    session = HTTP( api_key="cx9GeLY3Lyezm2SY4C", api_secret="GrHSgZeLBnCI9X3qXGUnsLLJxjTjgsNH5xDQ")
    m = []
    m1 = []
    for i in range(col):
        a = session.get_kline(
            category="inverse",
            symbol=name,
            interval=str(dataframe),
            start=un - 1000 * 12000*5 * dataframe,
            end=un,
            limit=1000
        )
        un -= 1000 * 12000 * dataframe*5
        m += [[float(i[1]), float(i[4])] for i in a['result']['list'][::1]]
        print(i, len(m))
        if i % 250 == 249:
            for j in range(20):
                time.sleep(1)
                print("slept", j * 1 + 1)
    print("Export is ok, len:", len(m))
    df = pd.DataFrame({"close": m[::-1]})
    df.to_csv("data_bnbusdt_6000.csv")
    # print(m[::-1])
    return m[::-1]
def export_from_file(filename):
    df = list(pd.read_csv(filename)['close'])
    df = [eval(i) for i in df]
    return df

