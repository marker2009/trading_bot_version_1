from coins import *
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
        self.col_orders = 0
        self.side_glav = -1
        self.coin = coin
        self.order_now = self.calculate_sum_of_first_order()
        self.sum_order_now = self.order_now


    def open_first_orders(self):
        return [[1, 1, self.order_now], [1, -1, self.order_now]]

    def calculate_sum_of_first_order(self):
        summ = 0
        first = 1
        for i in range(8):
            summ += first
            first *= self.multiplicity
        return calc_sum((0.44 / (summ * 1 + summ * self.koff) * self.deposit) / 2, self.coin) * 2

    def calc_next_order(self, order_sum):
        self.sum_order_now += calc_sum((self.order_now * self.multiplicity) / 2, self.coin) * 2
        return order_sum * self.multiplicity

    def what_to_do_normal(self, order_info):
        # print(time.time()- self.time)
        if self.col_orders >= 7:
            return [[0]]
        delta_time = time.time() - self.time
        if delta_time > self.need_delta_time:
            if self.is_first_order:
                if order_info[0]['spec_pnl'] > self.step_buy[0]:
                    self.order_now = self.calc_next_order(self.order_now)
                    self.is_first_order = False
                    self.side_glav = 1
                    self.col_orders += 1
                    self.time = time.time()
                    return [[1, 1, self.order_now], [-1, 0], [1, 0, self.sum_order_now * self.koff]]
                elif order_info[1]['spec_pnl'] > self.step_sell[0]:
                    self.order_now = self.calc_next_order(self.order_now)
                    self.is_first_order = False
                    self.side_glav = 0
                    self.col_orders += 1
                    self.time = time.time()
                    return [[1, 0, self.order_now], [-1, 1], [1, 1, self.sum_order_now * self.koff]]
            else:
                if self.side_glav == 1:
                    if order_info[0]['spec_pnl'] > self.step_buy[self.col_orders]:
                        self.order_now = self.calc_next_order(self.order_now)
                        self.col_orders += 1
                        self.time = time.time()
                        return [[1, 1, self.order_now], [-1, 0], [1, 0, self.sum_order_now * self.koff]]
                else:
                    if order_info[1]['spec_pnl'] > self.step_sell[self.col_orders]:
                        self.order_now = self.calc_next_order(self.order_now)
                        self.col_orders += 1
                        self.time = time.time()
                        return [[1, 0, self.order_now], [-1, 1], [1, 1, self.sum_order_now * self.koff]]

        return [[0]]

    def reformat(self, x):
        if x == 0:
            return -1
        else:
            return 1

    def what_to_do_unnormal(self, order_info):
        if self.col_orders >= 7:
            return [[0]]
        if self.is_first_order:
            if order_info[0]['spec_pnl'] > self.unnormal_price_move:
                self.order_now = self.calc_next_order(self.order_now)
                self.time = time.time()
                self.side_glav = 1
                self.is_first_order = False
                self.col_orders += 1
                orders.add_take_or_stop("unnormal_move " + str(self.side_glav) + " " + str(self.is_first_order))
                return [[1, 1, self.order_now], [-1, 0], [1, 0, self.sum_order_now * self.koff]]
            elif order_info[1]['spec_pnl'] > self.unnormal_price_move:
                self.order_now = self.calc_next_order(self.order_now)
                self.time = time.time()
                self.side_glav = 0
                self.is_first_order = False
                self.col_orders += 1
                orders.add_take_or_stop("unnormal_move " + str(self.side_glav) + " " + str(self.is_first_order))
                return [[1, 0, self.order_now], [-1, 1], [1, 1, self.sum_order_now * self.koff]]
        else:
            if order_info[1 - self.side_glav]['spec_pnl'] > self.unnormal_price_move:
                self.order_now = self.calc_next_order(self.order_now)
                self.time = time.time()
                self.col_orders += 1
                orders.add_take_or_stop("unnormal_move " + str(self.side_glav) + " " + str(self.is_first_order))
                if 1 - self.side_glav == 1:
                    return [[1, 0, self.order_now], [-1, 1], [1, 1, self.sum_order_now * self.koff]]
                return [[1, 1, self.order_now], [-1, 0], [1, 0, self.sum_order_now * self.koff]]

        return [[0]]
