import time as tm

timm = tm.time()
from visual_backtest import *

print(time.time())
m2 = export_from_file("data/data_ltcusdt_6000.csv")[:]
# m2 = export(1, "USDT", 1200)
print(m2[-1], m2[0])
m = [i[0] for i in m2]
from work_with_str6 import *

clas = work_1(["A7hKrcISyhFZdzddCZ"], ["hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI"])
leverage = 20
tks = 1
mas_1 = [2,3,3,3,5,5,6]
mas_2 = mas_1[::]
summm = 2000
stop = 15
volumes_glav = [0.1, 0.2, 0.4, 0.88, 1.93, 4.63, 12.04, 31.3]
print(sum(volumes_glav) * 0.75)
volumes_hedge = [0.1, 0.15]
su = 0.3
for i in range(len(volumes_glav) - 2):
    su += volumes_glav[i + 2]
    volumes_hedge.append(su / 2)
# volumes_hedge[-1] *= 8/5
print(volumes_hedge)
orders.summ = summm
clas.add_user("", "", "ETCUSDT", leverage,
              [i * 1.2 * leverage for i in mas_1], [i * leverage for i in mas_2], 2,
              summm * leverage,
              60 * 60, 10 * leverage, "marker", tks * leverage, stop * leverage, False, tks,
              volumes_glav, volumes_hedge,
              {"ETCUSDT": float(m[0])})

print(time.time())
col = 0
mi = 10 ** 1000
ds = []
ma = 0
for i in range(len(m)):
    if i % 10000 == 0:
        print(i)
    if time.time() in [382560, 382620, 382680]:
        print(m[i])
    if time.time() % 3600 == 0:
        orders.oun = 0
    ma = max(ma, orders.oun)
    clas.obxod({"ETCUSDT": float(m[i])})
    time.add_time(60)
    col += 1
    mi = min(mi, orders.summ)
    ds.append(orders.summ)
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
