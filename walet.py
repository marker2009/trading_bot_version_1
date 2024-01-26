class Wallet:
    def __init__(self, summ):
        self.sum = summ
        self.trades = []
        self.ids = []

    def prepare_data(self, data):
        pass

    def return_sum(self):
        return self.sum

    def open_trade(self, dir, price, col, leverage, take_profit=20, stop_loss=-10):
        self.trades.append([price, col, dir, take_profit, stop_loss, leverage])
        self.ids.append(len(self.trades) - 1)
        return len(self.trades) - 1

    def get_open_trades(self):
        m = []
        for i in range(len(self.trades)):
            if i in self.ids:
                m.append(self.trades[i])
        return m

    def get_profit(self, id, price, comm=0.055 * 0.01):
        buf = self.trades[id]
        col = buf[1]
        paid = col * buf[0] * comm
        plus = (price - buf[0]) * col * buf[2]
        paid1 = col * price * comm
        plus = plus - paid - paid1
        return (plus)

    def get_pnl(self, id, price):
        buf = self.trades[id]
        col = buf[1]
        sum = (col / buf[5]) * buf[0]
        plus = self.get_profit(id, price, comm=0)
        return (plus / sum) * 100

    def close_trade_take_or_stop(self, id, istake=0):
        buf = self.trades[id]
        if istake == 0:

            stop = buf[4]
            sum = (buf[1] / buf[5]) * buf[0]
            real_stop = stop / 100
            minus = sum * real_stop
            self.ids.pop(self.ids.index(id))
            self.sum += (minus - 2 * 0.055 * 0.01 * sum * buf[5])
            return (minus - 2 * 0.055 * 0.01 * sum * buf[5])
        else:
            take = buf[3]
            sum = (buf[1] / buf[5]) * buf[0]
            real_take = take / 100
            profit = sum * real_take
            self.ids.pop(self.ids.index(id))
            self.sum += (profit - 2 * 0.055 * 0.01 * sum * buf[5])
            return (profit - 2 * 0.055 * 0.01 * sum * buf[5])

    def close_trade(self, id, price):
        self.ids.pop(self.ids.index(id))
        self.sum += self.get_profit(id, price)
        return self.get_profit(id, price)

    def model_trade(self, ids, data):
        buf = self.trades[ids]
        take = buf[3]
        stop = buf[4]

        col = 0
        for i in data:
            col += 1
            if self.get_pnl(ids, i) > take:
                self.close_trade_take_or_stop(ids, 1)
                return 1
            elif self.get_pnl(ids, i) < stop:
                self.close_trade_take_or_stop(ids, 0)
                return -1
        self.close_trade(ids, data[-1])
        return 0
