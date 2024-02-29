import time as tm

from futures_positions_without_bybit import *
# from strategy_with_specially_time import *
from trading_bot_version_1.str7 import *


def get_data(price, price1):
    return (price + price1) / 2


class work_1:
    def __init__(self, system_apis, system_secret_apis):
        self.system_apis = system_apis
        self.system_secret_apis = system_secret_apis
        self.system_sessions = []
        self.tokens = []
        self.sides = []
        self.users = []
        self.layers_long = []
        self.layers_short = []
        self.unnormal_moves = []
        self.strateges = []
        self.deposits = []
        self.times = []
        self.coins = []
        self.short = []
        self.long = []
        self.multiplicity = []
        self.takes = []
        self.stops = []
        self.take_price = []
        self.stop_price = []
        self.layers = []
        self.leverage = []
        self.orders = []
        self.pers_data = []
        self.need_adds = []
        self.need_to_delete = []
        self.is_first = []
        self.op = 0

        self.sum = 0
        self.col = 0

    def do(self, buf, i, flag, coins):
        if buf != [[0]] and buf != None:
            print(buf, "buf")
            flag = True
            self.orders.append(buf + [0])
            for j in buf:
                print(j, "j in buf", self.coins, coins)

                if j[0] == -1:
                    if j[1] == 1:
                        if self.short[i] == -1:
                            # print("Error_short:", i, buf)
                            pass
                        else:
                            self.users[i].close_short_order(self.short[i], coins[self.coins[i]])
                            # print("Close is ok")
                            self.long[i] = 0
                            self.short[i] = -1
                    else:
                        if self.long[i] == -1:
                            # print("Error_long:", i, buf)
                            pass
                        else:
                            self.users[i].close_long_order(self.long[i], coins[self.coins[i]])
                            # print("Close_long is ok")
                            self.short[i] = 0
                            self.long[i] = -1
                elif j[0] == 1:
                    j[2] = calc_sum(j[2] / coins[self.coins[i]], self.coins[i])
                    print("summ of order", j[1], j[2])
                    if j[1] == 1:
                        if self.short[i] == -1:
                            self.short[i] = self.users[i].open_short_order(j[2], coins[self.coins[i]])
                            # print("Open short order is ok")
                        else:
                            print("want_to_sell_more")
                            self.users[i].sell_more(self.short[i], coins[self.coins[i]], j[2])
                            # print("sell more is ok")
                    else:
                        if self.long[i] == -1:
                            self.long[i] = self.users[i].open_long_order(j[2], coins[self.coins[i]])
                            # print("Open long order is OK")
                        else:
                            self.users[i].buy_more(self.long[i], coins[self.coins[i]], j[2])
                            # print("Buy more is OK")

        return flag

    def add_user(self, api, api_secret, coin, leverage, layers_long, layers_short, multiplicity, deposit, delta_time,
                 unnormal_move, token, take, stop, no_short, tks, volumes_glav, volumes_hedge, coins):
        print("start_now", token, coins[coin], self.sum / self.col if self.col != 0 else 0)
        self.is_first.append(True)
        orders.add_take_or_stop("start ")
        deposit = orders.summ * leverage
        self.pers_data.append(
            [api, api_secret, coin, leverage, layers_long, layers_short, multiplicity, deposit, delta_time,
             unnormal_move, token, take, stop, no_short, tks, volumes_glav, volumes_hedge])
        self.op += 1
        self.tokens.append(token)
        self.users.append(futures_positions(api, api_secret, leverage, coin))
        self.layers_short.append(layers_short)
        self.layers_long.append(layers_long)
        self.multiplicity.append(multiplicity)
        self.deposits.append(deposit)
        self.times.append(delta_time)
        self.unnormal_moves.append(unnormal_move)
        self.coins.append(coin)
        self.layers.append(coins[coin])
        self.sides.append(-1)
        self.takes.append(take)
        self.stops.append(stop)
        self.leverage.append(leverage)
        self.take_price.append(None)
        self.stop_price.append(None)
        self.short.append(-1)
        self.long.append(-1)
        print([layers_long, layers_short, delta_time, unnormal_move, deposit, coin, volumes_glav, volumes_hedge])
        self.strateges.append(
            strategy(layers_long, layers_short, delta_time, unnormal_move, deposit, coin, volumes_glav, volumes_hedge))
        buf = self.strateges[-1].open_first_orders()
        self.do(buf, len(self.strateges) - 1, True, coins)

        i = len(self.users) - 1

        return len(self.users) - 1

    def delete(self):
        for i in self.need_to_delete:
            self.delete_user(i[0], i[1])

    def set_take(self, i, side, data):
        res = get_data(data[0]['average_price'], data[1]['average_price'])
        koff = 1 / self.leverage[i]
        self.take_price[i] = res * (1 + koff * ((self.takes[i]) / 100 if side == 1 else (-1 * (self.takes[i] / 100))))
        print("sett_take", self.take_price, res, self.takes[i],
              (1 + ((self.takes[i]) / 100 if side == 0 else (-1 * (self.takes[i] / 100)))))

    def set_stop(self, last_price, i):
        if self.strateges[i].col_orders == 7:
            side = self.sides[i]
            koff = 1 / self.leverage[i]
            self.stop_price[i] = last_price * (
                        1 + koff * ((self.stops[i]) / 100 if side == 1 else (-1 * (self.stops[i] / 100))))
            print("sett_stop", self.stop_price, last_price)

        pass

    def add(self):
        for i in self.need_adds:
            self.add_user(*i[0], i[1])

    def obxod(self, coins):
        # coins = {coin:price}
        st = tm.time()
        for i in range(len(self.users)):
            # print(self.sides, self.takes, self.stops, self.take_price, self.stop_price)
            if self.in_need_to_close_take_or_stop(i, coins[self.coins[i]]):
                # print("close_orders_take_or_stop")
                if self.short[i] == -1:
                    # print("Bad error in close_short")
                    pass
                else:
                    self.users[i].close_short_order(self.short[i], coins[self.coins[i]])
                    self.long[i] = 0
                if self.long[i] == -1:
                    # print("Bad error in close_long")
                    pass
                else:
                    self.users[i].close_long_order(self.long[i], coins[self.coins[i]])
                    self.short[i] = 0
                self.short[i] = -1
                self.long[i] = -1
                self.need_to_delete.append([self.tokens[i], coins])
                self.need_adds.append([self.pers_data[i], coins])
                continue
            orders_info = [{'spec_pnl': 0}, {'spec_pnl': 0}]
            order_info = self.users[i].get_open_orders(coins[self.coins[i]])

            orders_info1 = [{'volume': 0, "price": 0}, {'volume': 0, "price": 0}]
            for j in order_info:
                bufs = int(j['side'] * (-0.5) + 0.5)
                orders_info[bufs]['spec_pnl'] = j['spec_pnl']
                orders_info1[bufs]['volume'] = j['volume']
                orders_info1[bufs]['price'] = j['average_price']
                orders_info1[bufs]['last_price'] = j['last_price']
            flag = False
            buf = self.strateges[i].what_to_do_unnormal(orders_info, orders_info1, coins[self.coins[i]])
            flag = self.do(buf, i, flag, coins)
            # print("start_unnormal")
            buf = self.strateges[i].what_to_do_normal(orders_info, orders_info1, coins[self.coins[i]], order_info)
            flag = self.do(buf, i, flag, coins)
            self.sides[i] = self.strateges[i].side_glav
            if flag:
                print(orders_info, orders_info1)
                if self.sides[i] != -1 and flag:
                    buf = self.take_price[i]
                    if self.sides[i] == 0:
                        res = get_res(self.users[i].get_open_orders()[self.short[i]]['average_price'],
                                      self.users[i].get_open_orders()[self.long[i]]['average_price'],
                                      self.users[i].get_open_orders()[self.long[i]]['volume'],
                                      self.users[i].get_open_orders()[self.short[i]]['volume'], 0)
                        self.take_price[i] = res*(1 + self.takes[i] / self.leverage[i] / 100)
                        print("ttk", res, (1 + self.takes[i] / self.leverage[i] / 100))
                        # self.stop_price[i] = self.layers[i] * (100 - self.stops[i] / self.leverage) / 100
                    else:
                        res = get_res(self.users[i].get_open_orders()[self.long[i]]['average_price'],
                                      self.users[i].get_open_orders()[self.short[i]]['average_price'],
                                      self.users[i].get_open_orders()[self.short[i]]['volume'],
                                      self.users[i].get_open_orders()[self.long[i]]['volume'], 1)
                        print("ttk", res,(1 - self.takes[i] / self.leverage[i] / 100))
                        self.take_price[i] = res*(1 - self.takes[i] / self.leverage[i] / 100)
                        # self.stop_price[i] = self.layers[i] * (100 + self.stops[i] / self.leverage) / 100
                    orders.add_take_or_stop("set_take=" + str(self.take_price[i]) + str(self.sides[i]))
                if self.strateges[i].col_orders >= len(self.strateges[i].step_sell) and self.stop_price[i] == None:
                    print("stop", self.deposits)
                    if self.sides[i] == 0:
                        # self.take_price[i] = self.layers[i] * (100 + self.takes[i] / self.leverage) / 100
                        self.stop_price[i] = self.users[i].get_open_orders()[self.long[i]]['last_price'] * (
                                100 - self.stops[i] / self.leverage[i]) / 100
                    else:
                        # self.take_price[i] = self.layers[i] * (100 - self.takes[i] / self.leverage) / 100
                        self.stop_price[i] = self.users[i].get_open_orders()[self.short[i]]['last_price'] * (
                                100 + self.stops[i] / self.leverage[i]) / 100
                    orders.add_take_or_stop(
                        "set stop = " + str(self.stop_price[i]) + " side: " + str(self.sides[i]) + " last_price:" + str(
                            self.users[i].get_open_orders()[0]['last_price']) + " first_price" + str(
                            self.layers[i]) + " take:" + str(self.take_price[i]))

        self.delete()
        self.add()
        self.need_adds = []
        self.need_to_delete = []
        self.sum += tm.time() - st
        self.col += 1

    def close(self):
        pass

    def in_need_to_close_take_or_stop(self, i, price):
        if self.sides[i] == -1:
            return False
        if self.sides[i] == 0:
            if price >= self.take_price[i]:
                orders.add_take_or_stop("GOOD take long")
                print(self.users[i].get_open_orders(price))
                print("GOOD take long", self.strateges[i].col_orders, time.time(), self.take_price,
                      self.users[i].get_open_orders()[self.long[i]]['last_price'])
                return True
            if self.stop_price[i] != None and price < self.stop_price[i]:
                orders.add_take_or_stop("BAD stop long " + str(self.strateges[i].col_orders) + " " + str(
                    self.users[i].get_open_orders(price)) + str(self.layers[i]))
                print("BAD but STOP", time.time(), self.take_price)
                return True
        if self.sides[i] == 1:
            if self.stop_price[i] != None and price > self.stop_price[i]:
                print("BAD but STOP short", time.time(), self.take_price)
                orders.add_take_or_stop("BAD stop short " + str(self.strateges[i].col_orders) + " " + str(
                    self.users[i].get_open_orders(price)) + str(self.layers[i]))
                return True
            if price <= self.take_price[i]:
                print(self.users[i].get_open_orders(price))
                orders.add_take_or_stop("GOOD take short")
                print("GOOD take short", self.strateges[i].col_orders, time.time(), self.take_price,
                      self.users[i].get_open_orders()[self.short[i]]['last_price'])
                return True
        return False

    def delete_user(self, token, coins):
        print("delete_user", token, self.op)
        i = self.tokens.index(token)
        # print(self.short, self.long)
        if self.short[i] != -1:
            self.users[i].close_short_order(self.short[i], coins[self.coins[i]])
            self.long[i] = 0 if self.long[i] != -1 else -1
        if self.long[i] != -1:
            self.users[i].close_long_order(self.long[i], coins[self.coins[i]])
            self.short[i] = 0
        self.tokens.pop(i)
        self.users.pop(i)
        self.layers_short.pop(i)
        self.layers_long.pop(i)
        self.multiplicity.pop(i)
        self.deposits.pop(i)
        self.times.pop(i)
        self.unnormal_moves.pop(i)
        self.coins.pop(i)
        self.strateges.pop(i)
        self.long.pop(i)
        self.short.pop(i)
        self.layers.pop(i)
        self.sides.pop(i)
        self.takes.pop(i)
        self.stops.pop(i)
        self.leverage.pop(i)
        self.take_price.pop(i)
        self.stop_price.pop(i)
        self.is_first.pop(i)
