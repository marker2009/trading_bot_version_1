import json
import time as tm

from futures_positions import *
# from strategy_with_specially_time import *
from trading_bot_version_1.str7 import *

ol = 0
import mysql.connector


def get_data(price, price1):
    return (price + price1) / 2


def is_work(bot_id):
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("SELECT * from `bots` WHERE `id` = " + str(bot_id))
    cursor1.execute(query1)
    for i in cursor1:
        return i[2] == 1


class polsov:
    def __init__(self, api, api_secret, coin, leverage, layers_long, layers_short, multiplicity, deposit, delta_time,
                 unnormal_move, token, take, stop, no_short, tks, volumes_glav, volumes_hedge, coins):
        self.tokens = token
        self.users = futures_positions(api, api_secret, leverage, coin)
        self.layers_short = layers_short
        self.layers_long = layers_long
        self.multiplicity = multiplicity
        self.deposits = deposit
        self.times = delta_time
        self.unnormal_moves = unnormal_move
        self.coins = coin
        print(coin, "coin")
        self.layers = coins[coin]
        self.sides = -1
        self.takes = take
        self.stops = stop
        self.leverage = leverage
        self.take_price = None
        self.stop_price = None
        self.short = -1
        self.long = -1
        self.strateges = strategy(layers_long, layers_short, delta_time, unnormal_move, deposit, coin, volumes_glav, volumes_hedge)


def get_api(bot_id):
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("SELECT * from `apis` WHERE `id` = " + str(bot_id))
    cursor1.execute(query1)
    for i in cursor1:
        return i[2], i[3]


class work_1:
    def __init__(self, system_apis, system_secret_apis):
        mas = ["system_apis", "system_secret_apis"]
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
        self.apis = []
        self.secrets = []
        self.is_first = []
        self.polsovatel = []
        self.op = 0

        self.sum = 0
        self.col = 0

    def do(self, buf, i, flag, coins):
        if buf != [[0]] and buf != None:
            # print(buf, "buf")
            flag = True

            for j in buf:
                # print(j, "j in buf", self.coins, coins)

                if j[0] == -1:
                    if j[1] == 1:
                        if self.polsovatel[i].short == -1:
                            # print("Error_short:", i, buf)
                            pass
                        else:
                            self.polsovatel[i].users.close_short_order(self.polsovatel[i].short,
                                                                       coins[self.polsovatel[i].coins])
                            # print("Close is ok")
                            self.polsovatel[i].long = 0
                            self.polsovatel[i].short = -1
                    else:
                        if self.polsovatel[i].long == -1:
                            # print("Error_long:", i, buf)
                            pass
                        else:
                            self.polsovatel[i].users.close_long_order(self.polsovatel[i].long,
                                                                      coins[self.polsovatel[i].coins])
                            # print("Close_long is ok")
                            self.polsovatel[i].short = 0
                            self.polsovatel[i].long = -1
                elif j[0] == 1:
                    j[2] = calc_sum(j[2] / coins[self.polsovatel[i].coins], self.polsovatel[i].coins)
                    # print("summ of order", j[1], j[2])
                    if j[1] == 1:
                        if self.polsovatel[i].short == -1:
                            self.polsovatel[i].short = self.polsovatel[i].users.open_short_order(j[2], coins[
                                self.polsovatel[i].coins])
                            # print("Open short order is ok")
                        else:
                            # print("want_to_sell_more")
                            self.polsovatel[i].users.sell_more(self.polsovatel[i].short,
                                                               coins[self.polsovatel[i].coins], j[2])
                            # print("sell more is ok")
                    else:
                        if self.polsovatel[i].long == -1:
                            self.polsovatel[i].long = self.polsovatel[i].users.open_long_order(j[2], coins[
                                self.polsovatel[i].coins])
                            # print("Open long order is OK")
                        else:
                            self.polsovatel[i].users.buy_more(self.polsovatel[i].long, coins[self.polsovatel[i].coins],
                                                              j[2])
                            # print("Buy more is OK")

        return flag

    def get_deposit(self, api, api_secret):
        try:
            session = HTTP(api_key=api, api_secret=api_secret)
            buf = session.get_wallet_balance(accountType="CONTRACT")
            # print(buf)
            buf = buf['result']['list'][0]['coin'][0]['equity']

            return float(buf)
        except Exception as e:
            try:
                send_error(e, api)
            except:
                print("very bad in send error")
            return 0

    def add_user(self, api, api_secret, coin, leverage, layers_long, layers_short, multiplicity, deposit, delta_time,
                 unnormal_move, token, take, stop, no_short, tks, volumes_glav, volumes_hedge, coins):

        cnx = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                      host='quejutuni.beget.app',
                                      database='projectimperial')
        cursor = cnx.cursor()
        query = ("SELECT * from `bots` WHERE `id` = " + token)
        # print(query)
        cursor.execute(query)

        # print([i for i in cursor], "!!")
        for i in cursor:
            buf = json.loads(i[3].replace("\n", ""))
            token = str(i[0])
            api, api_secret = get_api(i[0])
            layers_short = [i * buf['leverage'] for i in buf['short_layers']]
            layers_long = [i * buf['leverage'] for i in buf['long_layers']]
            volumes_glav = [i for i in buf['volumes_glav']]
            volumes_hedge = [i for i in buf['volumes_hedge']]
            multiplicity = 2
            delta_time = buf['time']
            leverage = buf['leverage']
            coin = buf['coin']
            unnormal_move = [buf['pump'] * buf['leverage'], buf['dump'] * buf['leverage']]
            take = buf['take'] * buf['leverage']
            stop = buf['stop'] * buf['leverage']
            # print(token, api, api_secret, layers_long, layers_short, multiplicity, delta_time, leverage, coin,
            #       unnormal_move,
            #       take, stop)

        cursor.close()
        cnx.close()
        # print("start_now", token, coins)
        orders.add_take_or_stop("start ")
        deposit = self.get_deposit(api, api_secret) * leverage
        print(deposit, "deposit")


        self.op += 1
        self.polsovatel.append(polsov(*[api, api_secret, coin, leverage, layers_long, layers_short, multiplicity, deposit, delta_time,
             unnormal_move, token, take, stop, no_short, tks, volumes_glav, volumes_hedge], coins))
        self.polsovatel[-1].pers_data = (
            [api, api_secret, coin, leverage, layers_long, layers_short, multiplicity, deposit, delta_time,
             unnormal_move, token, take, stop, no_short, tks, volumes_glav, volumes_hedge])
        # print([layers_long, layers_short, delta_time, unnormal_move, deposit, coin, volumes_glav, volumes_hedge])

        buf = self.polsovatel[-1].strateges.open_first_orders()
        self.do(buf, len(self.polsovatel) - 1, True, coins)

        return len(self.polsovatel) - 1

    def delete(self):
        for i in self.need_to_delete:
            self.delete_user(i[0], i[1])

    def add(self):
        for i in self.need_adds:
            self.add_user(*i[0], i[1])

    def set_take(self, i, side, data):
        res = get_data(data[0]['average_price'], data[1]['average_price'])
        koff = 1 / self.polsovatel[i].leverage
        self.polsovatel[i].take_price = res * (1 + koff * (
            (self.polsovatel[i].takes) / 100 if side == 1 else (-1 * (self.polsovatel[i].takes / 100))))
        # print("sett_take", self.take_price, res, self.takes[i],
        #       (1 + ((self.takes[i]) / 100 if side == 0 else (-1 * (self.takes[i] / 100)))))

    def set_stop(self, last_price, i):
        if self.polsovatel[i].strateges.col_orders == 7:
            side = self.polsovatel[i].sides
            koff = 1 / self.polsovatel[i].leverage
            self.polsovatel[i].stop_price = last_price * (
                    1 + koff * (
                (self.polsovatel[i].stops) / 100 if side == 1 else (-1 * (self.polsovatel[i].stops / 100))))
            # print("sett_stop", self.stop_price, last_price)

        pass

    def obxod(self, coins):
        # coins = {coin:price}
        st = tm.time()
        for i in range(len(self.polsovatel)):
            if is_work(self.polsovatel[i].tokens):
                print("work")
                # print(self.sides, self.takes, self.stops, self.take_price, self.stop_price)
                if self.in_need_to_close_take_or_stop(i, coins[self.polsovatel[i].coins]):
                    # print("close_orders_take_or_stop")
                    if self.polsovatel[i].short == -1:
                        # print("Bad error in close_short")
                        pass
                    else:
                        self.polsovatel[i].users.close_short_order(self.polsovatel[i].short,
                                                                   coins[self.polsovatel[i].coins])
                        self.polsovatel[i].long = 0
                    if self.polsovatel[i].long == -1:
                        # print("Bad error in close_long")
                        pass
                    else:
                        self.polsovatel[i].users.close_long_order(self.polsovatel[i].long,
                                                                  coins[self.polsovatel[i].coins])
                        self.polsovatel[i].short = 0
                    self.polsovatel[i].short = -1
                    self.polsovatel[i].long = -1
                    self.need_to_delete.append([self.polsovatel[i].tokens, coins])
                    self.need_adds.append([self.polsovatel[i].pers_data, coins])
                    continue
                orders_info = [{'spec_pnl': 0}, {'spec_pnl': 0}]
                order_info = self.polsovatel[i].users.get_open_orders(coins[self.polsovatel[i].coins])

                orders_info1 = [{'volume': 0, "price": 0}, {'volume': 0, "price": 0}]
                for j in order_info:
                    bufs = int(j['side'] * (-0.5) + 0.5)
                    orders_info[bufs]['spec_pnl'] = j['spec_pnl']
                    orders_info1[bufs]['volume'] = j['volume']
                    orders_info1[bufs]['price'] = j['average_price']
                    orders_info1[bufs]['last_price'] = j['last_price']
                flag = False
                buf = self.polsovatel[i].strateges.what_to_do_unnormal(orders_info, orders_info1,
                                                                       coins[self.polsovatel[i].coins])
                flag = self.do(buf, i, flag, coins)
                # print("start_unnormal")
                buf = self.polsovatel[i].strateges.what_to_do_normal(orders_info, orders_info1,
                                                                     coins[self.polsovatel[i].coins], order_info)
                flag = self.do(buf, i, flag, coins)
                self.polsovatel[i].sides = self.polsovatel[i].strateges.side_glav
                if flag:
                    # print(orders_info, orders_info1)
                    if self.polsovatel[i].sides != -1 and flag:
                        buf = self.polsovatel[i].take_price
                        if self.polsovatel[i].sides == 0:
                            res = get_res(
                                self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].short]['average_price'],
                                self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].long]['average_price'],
                                self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].long]['volume'],
                                self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].short]['volume'], 0)
                            self.polsovatel[i].take_price = res * (
                                        1 + self.polsovatel[i].takes / self.polsovatel[i].leverage / 100)
                            # print("ttk", res, (1 + self.takes[i] / self.leverage[i] / 100))
                            # self.stop_price[i] = self.layers[i] * (100 - self.stops[i] / self.leverage) / 100
                        else:
                            res = get_res(
                                self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].long]['average_price'],
                                self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].short]['average_price'],
                                self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].short]['volume'],
                                self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].long]['volume'], 1)
                            # print("ttk", res, (1 - self.takes[i] / self.leverage[i] / 100))
                            self.polsovatel[i].take_price = res * (
                                        1 - self.polsovatel[i].takes / self.polsovatel[i].leverage / 100)
                            # self.stop_price[i] = self.layers[i] * (100 + self.stops[i] / self.leverage) / 100

                    if self.polsovatel[i].strateges.col_orders >= len(self.polsovatel[i].strateges.step_sell) and \
                            self.polsovatel[i].stop_price == None:
                        # print("stop", self.deposits)
                        if self.polsovatel[i].sides == 0:
                            # self.take_price[i] = self.layers[i] * (100 + self.takes[i] / self.leverage) / 100
                            self.polsovatel[i].stop_price = \
                            self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].long]['last_price'] * (
                                    100 - self.polsovatel[i].stops / self.polsovatel[i].leverage) / 100
                        else:
                            # self.take_price[i] = self.layers[i] * (100 - self.takes[i] / self.leverage) / 100
                            self.polsovatel[i].stop_price = \
                            self.polsovatel[i].users.get_open_orders()[self.polsovatel[i].short]['last_price'] * (
                                    100 + self.polsovatel[i].stops / self.polsovatel[i].leverage) / 100

            else:
                global ol
                ol += 1
                if ol % 1000 == 0:
                    print("stoppppppp")
        self.delete()
        self.add()
        self.need_adds = []
        self.need_to_delete = []
        self.sum += tm.time() - st
        self.col += 1

    def close(self):
        pass

    def in_need_to_close_take_or_stop(self, i, price):
        if self.polsovatel[i].sides == -1:
            return False
        if self.polsovatel[i].sides == 0:
            if price >= self.polsovatel[i].take_price:
                orders.add_take_or_stop("GOOD take long")
                # print(self.users[i].get_open_orders(price))
                # print("GOOD take long", self.strateges[i].col_orders, time.time(), self.take_price,
                #       self.users[i].get_open_orders()[self.long[i]]['last_price'])
                return True
            if self.polsovatel[i].stop_price != None and price < self.polsovatel[i].stop_price:
                orders.add_take_or_stop("BAD stop long " + str(self.polsovatel[i].strateges.col_orders) + " " + str(
                    self.polsovatel[i].users.get_open_orders(price)) + str(self.polsovatel[i].layers))
                # print("BAD but STOP", time.time(), self.take_price)
                return True
        if self.polsovatel[i].sides == 1:
            if self.polsovatel[i].stop_price != None and price > self.polsovatel[i].stop_price:
                # print("BAD but STOP short", time.time(), self.take_price)
                orders.add_take_or_stop("BAD stop short " + str(self.polsovatel[i].strateges.col_orders) + " " + str(
                    self.polsovatel[i].users.get_open_orders(price)) + str(self.polsovatel[i].layers))
                return True
            if price <= self.polsovatel[i].take_price:
                # print(self.users[i].get_open_orders(price))
                orders.add_take_or_stop("GOOD take short")
                # print("GOOD take short", self.strateges[i].col_orders, time.time(), self.take_price,
                #       self.users[i].get_open_orders()[self.short[i]]['last_price'])
                return True
        return False

    def delete_user(self, token, coins):
        print("delete_user", token, self.op)
        i = [self.polsovatel[i].tokens for i in range(len(self.polsovatel))].index(token)

        if self.polsovatel[i].short != -1:
            self.users[i].close_short_order(self.polsovatel[i].short, coins[self.polsovatel[i].coins])
            self.polsovatel[i].long = 0 if self.polsovatel[i].long != -1 else -1
        if self.polsovatel[i].long != -1:
            self.polsovatel[i].users.close_long_order(self.polsovatel[i].long, coins[self.polsovatel[i].coins])
            self.polsovatel[i].short = 0
        self.polsovatel.pop(i)

