from time_s import *


# pr = 64430
# apr = 69829
# v1 = 189
# v2 = 101
def al(prr, pr, apr, v1, v2):
    return (prr - apr) * v1 - (prr - pr) * v2


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


# print(get_res(10, 9, 10, 20, 1))
# print(al(76026 * 1.01, pr, apr,v1, v2))


class strategy:
    def __init__(self, step_buy, step_sell, delta_time, multiplicity, unnormal_price_move, deposit, coin):
        self.koff = 0.5
        self.step_buy = step_buy
        self.step_sell = step_sell
        self.need_delta_time = delta_time
        self.unnormal_price_move = unnormal_price_move
        self.time = time.time()
        self.deposit = deposit
        self.multiplicity = multiplicity
        self.is_first_order = True
        self.us = 0.44
        self.col_orders = 0
        self.side_glav = 0
        self.coin = coin
        self.volumes_long = [0.5, 1,2,4,8,19.2]
        self.volumes_short = [0]
        for i in range(1, len(self.volumes_long)):
            self.volumes_short.append(sum(self.volumes_long[:i + 1]) /2)
        print(self.volumes_short)
        self.volumes_short = [i / 100 * self.deposit / 2 for i in self.volumes_short]
        self.volumes_long = [i / 100 * self.deposit /2 for i in self.volumes_long]

    def open_first_orders(self):
        return [[1, 1, self.volumes_short[0]], [1, -1, self.volumes_long[0]]]

    def what_to_do_normal(self, order_info):
        # print(time.time()- self.time)
        # print(order_info, self.step_sell, self.step_buy, time.time() - self.time, self.need_delta_time, self.side_glav,
        #       order_info[0]['spec_pnl'] * -1, self.step_sell[self.col_orders] if self.col_orders != len(self.step_sell) else - 10, self.col_orders)
        if self.col_orders >= len(self.step_sell):
            return [[0]]
        delta_time = time.time() - self.time
        if delta_time > self.need_delta_time:
            if self.side_glav == 0:
                if order_info[0]['spec_pnl'] * -1 > self.step_sell[self.col_orders]:
                    self.col_orders += 1
                    self.time = time.time()
                    return [[1, 0, self.volumes_long[self.col_orders]], [-1, 1],
                            [1, 1, self.volumes_short[self.col_orders]]]

        return [[0]]

    def reformat(self, x):
        if x == 0:
            return -1
        else:
            return 1

    def what_to_do_unnormal(self, order_info):
        if self.col_orders >= len(self.step_sell):
            return [[0]]
        if order_info[0]['spec_pnl'] * -1 > self.unnormal_price_move:
            self.time = time.time()
            self.col_orders += 1
            orders.add_take_or_stop("unnormal_move " + str(self.side_glav) + " " + str(self.is_first_order))
            return [[1, 0, self.volumes_long[self.col_orders]], [-1, 1], [1, 1, self.volumes_short[self.col_orders]]]
        return [[0]]
