coins = ["LTCUSDT", "ETCUSDT", "MATICUSDT", "KSMUSDT", "LINKUSDT", "ADAUSDT", "MKRUSDT"]
lot = [1, 2, 0, 2, 1, 0, 3]
def up(number, col_of_digits):
    return (number * (10 ** col_of_digits) // 1) / (10 ** col_of_digits)
def calc_sum(sum, coin):
    return up(sum, lot[coins.index(coin)])
