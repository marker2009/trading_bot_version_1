from time_s import *

def up(number, col_of_digits):
    return (number * (10 ** col_of_digits) // 1) / (10 ** col_of_digits)

class order:
    def __init__(self, price, volume, side, coin, leverage):
        self.time = time.time()
        self.side = 1*side
        self.average_price = price
        self.volume = volume
        self.last_price = price
        self.coin = coin
        self.leverage = leverage
        orders.add_volume(volume*price)


    def buy_more(self, price, volume):
        self.average_price = up((self.average_price * self.volume + price * volume) / (self.volume + volume), 3)
        self.last_price = price
        self.volume = self.volume + volume
        orders.add_volume(volume*price)
        self.time = time.time()

    def get_data(self, price=-1, comm=0.055 * 0.01):
        return {
            'coin': self.coin,
            'side': self.side,
            'time': self.time,
            'last_price': self.last_price,
            'average_price': self.average_price,
            'volume': self.volume,
            'leverage': self.leverage,
            'pnl': self.get_pnl(price),
            'profit': self.get_profit(price, comm=comm),
            'spec_pnl': self.get_spec_pnl(price),
            'price':price
        }

    def get_profit(self, price, comm=0.055 * 0.01):
        volume = self.volume
        paid = volume * comm
        plus = (price - self.average_price) * volume * self.side
        paid1 = volume  * comm
        plus = plus - paid - paid1
        return (plus)

    def get_pnl(self, price):
        volume = self.volume
        #print([volume, self.leverage, self.average_price, '1'])
        sum = (volume / self.leverage) * self.average_price
        if sum == 0:
            return 0
        plus = self.get_profit(price, comm=0)
        return (plus / sum) * 100

    def get_spec_profit(self, price, comm=0.055 * 0.01):
        volume = self.volume
        paid = volume * comm
        plus = (price - self.last_price) * volume * self.side
        paid1 = volume * comm
        plus = plus - paid - paid1
        return (plus)

    def get_spec_pnl(self, price):
        volume = self.volume
        #print([volume, self.leverage, self.last_price, '1'])
        sum = (volume / self.leverage) * self.last_price
        if sum == 0:
            return 0
        plus = self.get_spec_profit(price, comm=0)
        return (plus / sum) * 100
