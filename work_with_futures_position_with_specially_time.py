from futures_positions_without_bybit import *
# from strategy_with_specially_time import *
from strategy_with_specially_time import *

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

    def add_user(self, api, api_secret, coin, leverage, layers_long, layers_short, multiplicity, deposit, delta_time,
                 unnormal_move, token, take, stop, no_short,tks,  coins):
        print("start_now", token,coins[coin])
        orders.add_take_or_stop("start ")
        deposit = orders.summ * leverage
        self.pers_data.append(
            [api, api_secret, coin, leverage, layers_long, layers_short, multiplicity, deposit, delta_time,
             unnormal_move, token, take, stop, no_short, tks])

        self.tokens.append(token)
        self.users.append(futures_positions(api, api_secret, leverage, coin))
        self.layers_short.append(layers_short)
        self.layers_long.append(layers_long)
        self.multiplicity.append(multiplicity)
        self.deposits.append(deposit)
        self.times.append(delta_time)
        self.unnormal_moves.append(unnormal_move)
        self.coins.append(coin)
        self.strateges.append(
            strategy(layers_long, layers_short, delta_time, multiplicity, unnormal_move, deposit, coin))
        buf = self.strateges[-1].open_first_orders()
        buf[0][2] = buf[0][2] / coins[coin]
        buf[0][2] = calc_sum(buf[0][2], coin)
        self.long.append(self.users[-1].open_long_order(buf[0][2], coins[coin]))
        if no_short == False:
            self.short.append(self.users[-1].open_short_order(buf[0][2], coins[coin]))
        else:
            self.short.append(self.users[-1].open_short_order(0.01, coins[coin]))
        self.layers.append(coins[coin])
        self.sides.append(-1)
        self.takes.append(take)
        self.stops.append(stop)
        self.leverage.append(leverage)
        self.take_price.append(None)
        self.stop_price.append(None)

        return len(self.users) - 1

    def delete(self):
        for i in self.need_to_delete:
            self.delete_user(i[0], i[1])

    def add(self):
        for i in self.need_adds:
            self.add_user(*i[0], i[1])

    def obxod(self, coins):
        # coins = {coin:price}
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
            for j in order_info:
                if j['side'] == -1:
                    orders_info[1]['spec_pnl'] = j['spec_pnl']
                else:
                    orders_info[0]['spec_pnl'] = j['spec_pnl']
            flag = False
            # print(*orders_info, sep=" \n")
            # print("start_normal")
            buf = self.strateges[i].what_to_do_unnormal(orders_info)
            # print("end_normal")
            # print(buf, "un")
            if buf != [[0]]:
                flag = True
                self.orders.append(buf + [0])
                for j in buf:
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
                        if j[1] == 1:
                            if self.short[i] == -1:
                                self.short[i] = self.users[i].open_short_order(j[2], coins[self.coins[i]])
                                # print("Open short order is ok")
                            else:
                                self.users[i].sell_more(self.short[i], coins[self.coins[i]], j[2])
                                # print("sell more is ok")
                        else:
                            if self.long[i] == -1:
                                self.long[i] = self.users[i].open_long_order(j[2], coins[self.coins[i]])
                                # print("Open long order is OK")
                            else:
                                self.users[i].buy_more(self.long[i], coins[self.coins[i]], j[2])
                                # print("Buy more is OK")
            # print("start_unnormal")
            buf = self.strateges[i].what_to_do_normal(orders_info)
            # print("end_unnormal")
            # print(buf)
            if buf != [[0]]:
                flag = True
                orders.oun += 1
                self.orders.append(buf + [-1])
                for j in buf:
                    if j[0] == -1:
                        if j[1] == 1:
                            if self.short[i] == -1:
                                # print("Error_short:", i, buf)
                                pass
                            else:
                                self.users[i].close_short_order(self.short[i], coins[self.coins[i]])
                                self.long[i] = 0
                                self.short[i] = -1
                        else:
                            if self.long[i] == -1:
                                # print("Error_long:", i, buf)
                                pass
                            else:
                                self.users[i].close_long_order(self.long[i], coins[self.coins[i]])
                                self.short[i] = 0
                                self.long[i] = -1
                    elif j[0] == 1:
                        j[2] = calc_sum(j[2] / coins[self.coins[i]], self.coins[i])
                        if j[1] == 1:
                            if self.short[i] == -1:
                                self.short[i] = self.users[i].open_short_order(j[2], coins[self.coins[i]])
                            else:
                                self.users[i].sell_more(self.short[i], coins[self.coins[i]], j[2])
                        else:
                            if self.long[i] == -1:
                                self.long[i] = self.users[i].open_long_order(j[2], coins[self.coins[i]])
                            else:
                                self.users[i].buy_more(self.long[i], coins[self.coins[i]], j[2])

            self.sides[i] = self.strateges[i].side_glav
            if self.sides[i] != -1 and flag:
                buf = self.take_price[i]
                if self.sides[i] == 0:
                    res = get_res(self.users[i].get_open_orders()[self.long[i]]['last_price'],
                                  self.users[i].get_open_orders()[self.long[i]]['average_price'],
                                  self.users[i].get_open_orders()[self.long[i]]['volume'],
                                  self.users[i].get_open_orders()[self.short[i]]['volume'], 0)
                    self.take_price[i] = res * ((100 + self.takes[i] / self.leverage[i]) / 100)
                    # self.stop_price[i] = self.layers[i] * (100 - self.stops[i] / self.leverage) / 100
                else:
                    res = get_res(self.users[i].get_open_orders()[self.short[i]]['last_price'],
                                  self.users[i].get_open_orders()[self.short[i]]['average_price'],
                                  self.users[i].get_open_orders()[self.short[i]]['volume'],
                                  self.users[i].get_open_orders()[self.long[i]]['volume'], 1)
                    self.take_price[i] = res * ((100 - self.takes[i] / self.leverage[i]) / 100)
                if buf != self.take_price[i]:
                    print(self.take_price[i])
                    # self.stop_price[i] = self.layers[i] * (100 + self.stops[i] / self.leverage) / 100
                orders.add_take_or_stop("set_take=" + str(self.take_price[i]) + str(self.sides[i]))
            if self.strateges[i].col_orders > 6 and self.stop_price[i] == None:
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
                    self.users[i].get_open_orders(price)))
                print("BAD but STOP", time.time())
                return True
        if self.sides[i] == 1:
            if self.stop_price[i] != None and price > self.stop_price[i]:
                print("BAD but STOP short", time.time())
                orders.add_take_or_stop("BAD stop short " + str(self.strateges[i].col_orders) + " " + str(
                    self.users[i].get_open_orders(price)))
                return True
            if price <= self.take_price[i]:
                print(self.users[i].get_open_orders(price))
                orders.add_take_or_stop("GOOD take short")
                print("GOOD take short", self.strateges[i].col_orders, time.time(), self.take_price,
                      self.users[i].get_open_orders()[self.short[i]]['last_price'])

                return True
        return False

    def delete_user(self, token, coins):
        print("delete_user", token)
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
