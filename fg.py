import time
import dill
import time as tm
from bybit_1 import *

timm = tm.time()
from visual_backtest import *

print(time.time())
m2 = export_from_file("data_ltcusdt_6000.csv")[400000:]
# m2 = export(1, "USDT", 1200)
print(m2[-1], m2[0])
m = [i[0] for i in m2]
from work_with_futures_position_with_specially_time import *

# from work_with_fhird import *

#
# orde = [[], []]
# #m1 = [[] for i in range(len(m))]
clas = work_1(["A7hKrcISyhFZdzddCZ"], ["hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI"])
leverage = 25
# tks = [4, 4, 5, 6, 10]
tks = 0.8
mas_1 = [2, 3, 3, 3, 5, 5, 6]
mas_2 = mas_1[::]
summm = 2000
orders.summ = summm
clas.add_user("A7hKrcISyhFZdzddCZ", "hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI", "ETCUSDT", leverage,
              [i * 1.2 * leverage for i in mas_1], [i * leverage for i in mas_2], 2,
              summm * leverage,
              60 * 60, 10 * leverage, "marker", 5 * leverage, 15 * leverage, False, tks, {"ETCUSDT": float(m[0])})
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
# pip install dill --user
