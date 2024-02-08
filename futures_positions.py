from pybit.unified_trading import HTTP
from order import *
from coins import *

from errors import *


class futures_positions:
    # не забывать переводить в режим хэджирования
    def __init__(self, api, secret_api, leverage, coin):
        self.api = api
        self.secret_api = secret_api
        self.session = HTTP(
            api_key=api,
            api_secret=secret_api,
            recv_window=5000
        )
        self.orders = []
        self.leverage = leverage
        self.coin = coin
        for i in range(5):
            if self.change_hedge(self.coin) == None:
                break
        for i in range(5):
            if None == self.change_leverage(self.leverage, self.coin):
                break

    def change_leverage(self, leverage, coin):
        try:
            self.session = HTTP(
                api_key=self.api,
                api_secret=self.secret_api
            )
            buf = self.session.set_leverage(
                category="inverse",
                symbol=coin,
                buyLeverage=str(leverage),
                sellLeverage=str(leverage),
            )
            # print(buf)
        except Exception as e:
            return -1

    def change_hedge(self, coin):
        try:
            self.session = HTTP(
                api_key=self.api,
                api_secret=self.secret_api
            )
            print(self.session.switch_position_mode(
                category="inverse",
                symbol=coin,
                mode=3,
            ))
            # print(buf)
        except Exception as e:
            return -1

    def open_short_order(self, volume, price):
        orders.append([self.coin, price, volume, 0])
        coin = self.coin
        volume = calc_sum(volume, coin)
        for i in range(3):
            try:
                self.session = HTTP(
                    api_key=self.api,
                    api_secret=self.secret_api
                )
                buf = self.session.place_order(
                    category="inverse",
                    symbol=coin,
                    side="Sell",
                    orderType="Market",
                    qty=volume,
                    positionIdx=2,
                    isLeverage=1,
                )
                self.orders.append(order(price, volume, -1, coin, self.leverage))
                return len(self.orders) - 1
            except Exception as e:
                print(e)
                pass
        send_error("dont_open_order:" + str(['inverse', coin, 'Sell', 'Market', volume, 2, 1]), self.api)

    def open_long_order(self, volume, price):
        orders.append([self.coin, price, volume, 1])
        coin = self.coin
        volume = calc_sum(volume, coin)
        for i in range(3):
            try:
                self.session = HTTP(
                    api_key=self.api,
                    api_secret=self.secret_api
                )
                buf = self.session.place_order(
                    category="inverse",
                    symbol=coin,
                    side="Buy",
                    orderType="Market",
                    qty=volume,
                    positionIdx=1,
                    isLeverage=1,
                )
                self.orders.append(order(price, volume, 1, coin, self.leverage))
                return len(self.orders) - 1
            except Exception as e:
                print(e)
                pass
        send_error("dont_open_order:" + str(['inverse', coin, 'Buy', 'Market', volume, 1, 1]), self.api)

    def get_open_orders(self, price=-1):
        orders = self.orders
        orders = [i.get_data(price=price) for i in orders]
        return orders

    def buy_more(self, order_id, price, volume):
        orders.append([self.orders[order_id].get_data(price)['coin'], price, volume, 3])
        coin = self.orders[order_id].get_data(price)['coin']
        volume = calc_sum(volume, coin)
        for i in range(3):
            try:
                buf = self.session.place_order(
                    category="inverse",
                    symbol=coin,
                    side="Buy",
                    orderType="Market",
                    qty=volume,
                    positionIdx=1,
                    isLeverage=1
                )
                self.orders[order_id].buy_more(price, volume)
                return
            except:
                pass
        send_error("dont_open_order(dokup):" + str(['inverse', coin, 'Buy', 'Market', volume, 1, 1]), self.api)

    def sell_more(self, order_id, price, volume):
        orders.append([self.orders[order_id].get_data(price)['coin'], price, volume, 2])
        coin = self.orders[order_id].get_data(price)['coin']
        volume = calc_sum(volume, coin)
        for i in range(3):
            try:

                buf = self.session.place_order(
                    category="inverse",
                    symbol=coin,
                    side="Sell",
                    orderType="Market",
                    qty=volume,
                    positionIdx=2,
                    isLeverage=1
                )
                self.orders[order_id].buy_more(price, volume)
                return None
            except:

                pass
        send_error("dont_open_order(dosell):" + str(['inverse', coin, 'Sell', 'Market', volume, 2, 1]), self.api)

    def close_short_order(self, order_id, price):
        orders.update_summ(self.orders[order_id].get_data(price)['profit'])
        coin = self.orders[order_id].get_data(price)['coin']
        orders.append([self.coin, price, calc_sum(self.orders[order_id].get_data(price)['volume'], coin), 4])
        volume = calc_sum(self.orders[order_id].get_data(price)['volume'], coin)
        for i in range(3):
            try:
                buf = self.session.place_order(
                    category="inverse",
                    symbol=coin,
                    side="Buy",
                    orderType="Market",
                    qty=volume,
                    positionIdx=2,
                    isLeverage=1
                )
                buf = self.orders[order_id].get_profit(price)
                self.orders.pop(order_id)
                return buf
            except:
                pass
        send_error("dont_open_order(closeshort):" + str(['inverse', coin, 'Buy', 'Market', volume, 2, 1]), self.api)

    def close_long_order(self, order_id, price):
        orders.update_summ(self.orders[order_id].get_data(price)['profit'])
        coin = self.orders[order_id].get_data(price)['coin']
        volume = calc_sum(self.orders[order_id].get_data(price)['volume'], coin)
        orders.append([self.coin, price, calc_sum(self.orders[order_id].get_data(price)['volume'], coin), 5])
        for i in range(3):
            try:
                buf = self.session.place_order(
                    category="inverse",
                    symbol=coin,
                    side="Sell",
                    orderType="Market",
                    qty=volume,
                    positionIdx=1,
                    isLeverage=1
                )
                buf = self.orders[order_id].get_profit(price)
                self.orders.pop(order_id)
                return buf
            except:
                pass
        send_error("dont_open_order(close_long):" + str(['inverse', coin, 'Sell', 'Market', volume, 1, 1]), self.api)

# def open_short_order(self, volume, price):
#     coin = self.coin
#     volume = calc_sum(volume, coin)
#     buf = self.session.place_order(
#         category="inverse",
#         symbol=coin,
#         side="Sell",
#         orderType="Market",
#         qty=volume,
#         positionIdx=2,
#         isLeverage=1,
#         recv_window=5000
#     )
#     self.orders.append(order(price, volume, -1, coin, self.leverage))
#     return len(self.orders) - 1
#
# def open_long_order(self,  volume, price):
#
#     coin = self.coin
#     volume = calc_sum(volume, coin)
#     buf = self.session.place_order(
#         category="inverse",
#         symbol=coin,
#         side="Buy",
#         orderType="Market",
#         qty=volume,
#         positionIdx=1,
#         isLeverage=1,
#         recv_window=5000
#     )
#     self.orders.append(order(price, volume, 1, coin, self.leverage))
#     return len(self.orders) - 1
#
# def get_open_orders(self, price = -1):
#     orders = self.orders
#     orders = [i.get_data(price= price) for i in orders]
#     return orders
#
# def buy_more(self, order_id, price, volume):
#     coin = self.orders[order_id].get_data(price)['coin']
#     volume = calc_sum(volume, coin)
#     buf = self.session.place_order(
#         category="inverse",
#         symbol=,
#         side="Buy",
#         orderType="Market",
#         qty=volume,
#         positionIdx=1,
#         isLeverage=1,
#         recv_window=5000
#     )
#     self.orders[order_id].buy_more(price, volume)
#
# def sell_more(self, order_id, price, volume):
#     coin = self.orders[order_id].get_data(price)['coin']
#     volume = calc_sum(volume, coin)
#     buf = self.session.place_order(
#         category="inverse",
#         symbol=coin,
#         side="Sell",
#         orderType="Market",
#         qty=volume,
#         positionIdx=2,
#         isLeverage=1,
#         recv_window=5000
#     )
#     self.orders[order_id].buy_more(price, volume)
#
# def close_short_order(self, order_id, price):
#     coin = self.orders[order_id].get_data(price)['coin']
#     volume = calc_sum(self.orders[order_id].get_data(price)['volume'], coin)
#     buf = self.session.place_order(
#         category="inverse",
#         symbol=coin,
#         side="Buy",
#         orderType="Market",
#         qty=volume,
#         positionIdx=2,
#         isLeverage=1,
#         recv_window=5000
#     )
#     buf = self.orders[order_id].get_profit(price)
#     self.orders.pop(order_id)
#     return buf
#
# def close_long_order(self, order_id, price):
#     coin = self.orders[order_id].get_data(price)['coin']
#     volume = calc_sum(self.orders[order_id].get_data(price)['volume'], coin)
#     buf = self.session.place_order(
#         category="inverse",
#         symbol=coin,
#         side="Sell",
#         orderType="Market",
#         qty=volume,
#         positionIdx=1,
#         isLeverage=1,
#         recv_window=5000
#     )
#     buf = self.orders[order_id].get_profit(price)
#     self.orders.pop(order_id)
#     return buf
