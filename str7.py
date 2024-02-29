from time_s import *


# pr = 64430
# apr = 69829
# v1 = 189
# v2 = 101
def al(prr, pr, apr, v1, v2):
    return (prr - apr) * v1 - (prr - pr) * v2


def calc_last_order(glav_price, glav_volume, hedge_price, hedge_volume, price):
    # print(glav_price, glav_volume, hedge_price, hedge_volume, price)
    delta = 0.5
    for i in range(1, 100000):
        i = i / 100
        sr = (hedge_price * hedge_volume + price * i) / (hedge_volume + i)
        if abs(sr / glav_price - 1) * 100 < delta:
            print(abs(sr / glav_price - 1), i, sr, glav_price, "this is need info ")
            return i

    s = 0 / 0


def get_res(pr, apr, v1, v2, side):
    if side == 0:
        pr = pr * 100
        apr = apr * 100
        for i in range(int(min(pr, apr) / 2), int(max(pr, apr) * 2)):
            if al(i, pr, apr, v1, v2) >= 0:
                return i / 100
    else:
        pr = pr * 100
        apr = apr * 100
        for i in range(int(min(pr, apr) / 2), int(max(pr, apr) * 2), 1):
            if al(i, pr, apr, v1, v2) >= 0:
                return i / 100


def get_res(pr, apr, v1, v2, side):
    return (pr + apr) / 2

def al(prr, pr, apr, v1, v2):
    return (prr - apr) * v1 - (prr - pr) * v2
def get_res(pr, apr, v1, v2, side):
    if side == 0:
        pr = pr * 100
        apr = apr * 100
        for i in range(1, 1000000):
            if al(i, pr, apr,v1, v2) > 0:
                return i / 100
    else:
        pr = pr * 100
        apr = apr * 100
        for i in range(1, 1000000, 1):
            if al(i, pr, apr,v1, v2)  > 0:
                return i / 100
# print(get_res(10, 9, 10, 20, 1))
# print(al(76026 * 1.01, pr, apr,v1, v2))


class strategy:
    def __init__(self, step_buy, step_sell, delta_time, unnormal_price_move, deposit, coin, volumes_glav,
                 volumes_hedge):
        self.is_first = True
        koff = 1 / 2
        self.unnormal_move = unnormal_price_move
        # unnormal_price_move
        self.col_orders = 0
        self.side_glav = -1
        self.layers_long = step_buy
        self.step_buy = step_buy
        self.layers_short = step_sell
        self.step_sell = step_sell
        self.volumes_glav = volumes_glav
        self.volumes_hedge = volumes_hedge
        self.delta_time = delta_time
        self.glav = [i * deposit * koff / 100 for i in self.volumes_glav]
        self.hedge = [i * deposit * koff / 100 for i in self.volumes_hedge]
        # print(self.glav, self.hedge)
        self.save_time = time.time()

    def open_first_orders(self):
        return [[1, 1, self.glav[0]], [1, -1, self.hedge[0]]]

    def do_next(self):
        self.col_orders += 1
        self.save_time = time.time()

    def what_to_do_normal(self, order_info, orders_info, price, k):
        if time.time() - self.save_time >= self.delta_time:
            if self.is_first:
                mas = [order_info[i]['spec_pnl'] * -1 > (self.layers_long[0] if i == 0 else self.layers_short[0]) for i
                       in [0, 1]]
                if 1 in mas:
                    self.side_glav = mas.index(1)
                    self.do_next()
                    self.is_first = False
                    return [[1, self.side_glav, self.glav[self.col_orders]], [-1, 1 - self.side_glav],
                            [1, 1 - self.side_glav, self.hedge[self.col_orders]]]
            else:
                if self.col_orders >= len(self.layers_long):
                    return [[0]]
                if order_info[self.side_glav]['spec_pnl'] * -1 > (
                        self.layers_long[self.col_orders] if self.side_glav == 0 else self.layers_short[
                            self.col_orders]):
                    self.do_next()
                    return [[1, self.side_glav, self.glav[self.col_orders]], [-1, 1 - self.side_glav],
                            [1, 1 - self.side_glav, self.hedge[self.col_orders]]]
        return [[0]]

    def reformat(self, x):
        if x == 0:
            return -1
        else:
            return 1

    def what_to_do_unnormal(self, order_info, orders_info, price):
        if self.col_orders >= len(self.layers_long) or self.is_first == True:
            return [[0]]
        if order_info[self.side_glav]['spec_pnl'] * -1 > (self.unnormal_move[self.side_glav]):
            self.do_next()
            return [[1, self.side_glav, self.glav[self.col_orders]], [-1, 1 - self.side_glav],
                    [1, 1 - self.side_glav, self.hedge[self.col_orders]]]
        return [[0]]
