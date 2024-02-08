import time
import time as tm
from bybit_1 import *

timm = tm.time()
from visual_backtest import *

print(time.time())
m2 = export_from_file("data/data_ltcusdt_6000.csv")[:]
# m2 = export(1, "USDT", 1200)
print(m2[-1], m2[0])
m = [i[0] for i in m2]
from work_with_st4 import *

# from work_with_fhird import *

#
# orde = [[], []]
# #m1 = [[] for i in range(len(m))]
clas = work_1(["A7hKrcISyhFZdzddCZ"], ["hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI"])
leverage = 25
# tks = [4, 4, 5, 6, 10]
tks = 1
mas_1 = [6,10,10,14]
mas_2 = mas_1[::]
summm = 2000
orders.summ = summm
clas.add_user("A7hKrcISyhFZdzddCZ", "hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI", "ETCUSDT", leverage,
              [i * 1.2 * leverage for i in mas_1], [i * leverage for i in mas_2], 2,
              summm * leverage,
              60 * 60, 20 * leverage, "marker", 5 * leverage, 15 * leverage, False, tks, {"ETCUSDT": float(m[0])})
# time.add_time(3601)
# clas.obxod({"MATICUSDT": float(9.5)})
#
# time.add_time(3601)
# clas.obxod({"MATICUSDT": float(9)})
# time.add_time(3601)
#
# print(clas.takes, clas.take_price)
# print(clas.users[0].get_open_orders(10.07))
# print(clas.obxod({"MATICUSDT": float(10.07)}))
#
# print(orders.order)
# print(orders.summ)
print(time.time())
col = 0
mi = 10 ** 1000
ds = []
ma = 0
# and to load the session again:
# import dill                            #pip install dill --user
# filename = 'globalsave.pkl'
# dill.load_session(filename)
for i in range(len(m)):
    if i % 10000 == 0:
        print(i)
    if time.time() in [382560, 382620, 382680]:
        print(m[i])
    if time.time() % 3600 == 0:
        orders.oun = 0
    ma = max(ma, orders.oun)
    # clas.users[-1].session = HTTP(
    #     api_key="A7hKrcISyhFZdzddCZ",
    #     api_secret="hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI",
    # )
    # buf = session.get_tickers(
    #     category="inverse",
    #     symbol="KSMUSDT",
    # )['result']['list'][0]['lastPrice']
    # print(clas.users[-1].get_open_orders(price = m[i]))
    clas.obxod({"ETCUSDT": float(m[i])})
    time.add_time(60)
    col += 1
    mi = min(mi, orders.summ)
    ds.append(orders.summ)
    # if col % 10 == 0:
    #     print(clas.users[-1].get_open_orders(price=float(buf)), buf, clas.take_price)
print(orders.summ, 1)
print(mi)
print(clas.users[0].get_open_orders(m[-1]))
print(orders.order)
print(orders.summ)
print(mi)
print(ma)
print(tm.time() - timm)
from matplotlib import pyplot as plt

plt.plot([ds[i] for i in range(len(ds)) if i % 10 == 0])
plt.show()
print(orders.volume)
# orde = [[],[]]
# for i in orders.order:
#     if i[-2] %  2 == 0:
#         orde[0].append(i[-1] // 60)
#     else:
#         orde[1].append(i[-1] // 60)
# print(orde)
# crasota(m2, orde)
