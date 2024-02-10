from pybit.unified_trading import HTTP
from order import *
from coins import *


class futures_positions:
    # не забывать переводить в режим хэджирования
    def __init__(self, api, secret_api, leverage, coin):
        self.api = api
        self.secret_api = secret_api
        # self.session = HTTP(
        #     api_key=api,
        #     api_secret=secret_api,
        #     recv_window=5000
        # )
        self.orders = []
        self.leverage = leverage
        self.coin = coin
        col = 0
        while self.change_leverage(self.leverage, self.coin) != 1:
            col += 1
            if col == 10:
                break
            pass

    def change_leverage(self, leverage, coin):
        try:
            pass
        except Exception as e:
            return -1

    def open_short_order(self, volume, price):
        print("open_short")
        orders.append([self.coin, price, volume, 0])
        coin = self.coin
        volume = calc_sum(volume, coin)
        self.orders.append(order(price, volume, -1, coin, self.leverage))
        return len(self.orders) - 1

    def open_long_order(self, volume, price):
        print("open_long")
        orders.append([self.coin, price, volume, 1])
        coin = self.coin
        volume = calc_sum(volume, coin)
        self.orders.append(order(price, volume, 1, coin, self.leverage))
        return len(self.orders) - 1

    def get_open_orders(self, price=-1):
        orders = self.orders
        orders = [i.get_data(price=price) for i in orders]
        return orders

    def buy_more(self, order_id, price, volume):
        print("buy_more")
        orders.append([self.orders[order_id].get_data(price)['coin'], price, volume, 3])
        coin = self.orders[order_id].get_data(price)['coin']
        volume = calc_sum(volume, coin)
        self.orders[order_id].buy_more(price, volume)

    def sell_more(self, order_id, price, volume):
        print("sell_more")
        orders.append([self.orders[order_id].get_data(price)['coin'], price, volume, 2])
        coin = self.orders[order_id].get_data(price)['coin']
        volume = calc_sum(volume, coin)
        self.orders[order_id].buy_more(price, volume)

    def close_short_order(self, order_id, price):
        print("close_short")
        orders.update_summ(self.orders[order_id].get_data(price)['profit'])
        coin = self.orders[order_id].get_data(price)['coin']
        orders.append([self.coin, price, calc_sum(self.orders[order_id].get_data(price)['volume'], coin), 4])
        volume = calc_sum(self.orders[order_id].get_data(price)['volume'], coin)
        buf = self.orders[order_id].get_profit(price)
        self.orders.pop(order_id)
        return buf

    def close_long_order(self, order_id, price):
        print("close_long")
        orders.update_summ(self.orders[order_id].get_data(price)['profit'])
        coin = self.orders[order_id].get_data(price)['coin']
        volume = calc_sum(self.orders[order_id].get_data(price)['volume'], coin)
        orders.append([self.coin, price, calc_sum(self.orders[order_id].get_data(price)['volume'], coin), 5])
        buf = self.orders[order_id].get_profit(price)
        self.orders.pop(order_id)
        return buf
