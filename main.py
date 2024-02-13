def al(prr, pr, apr, v1, v2):
    return (prr - apr) * v1 - (prr - pr) * v2
def get_res(pr, apr, v1, v2, side):
    if side == 0:
        pr = pr * 100
        apr = apr * 100
        for i in range(int(apr), pr*2):
            if al(i, pr, apr,v1, v2) > 0:
                return i / 100
    else:
        pr = pr * 100
        apr = apr * 100
        for i in range(int(apr / 2), pr * 2):
            if al(i, pr, apr,v1, v2)  > 0:
                return i / 100
print(get_res(1,1,1,1,1))
# print(get_res(54.62, 54.183,  1.25, 0.62, 1))
# print(get_res(51.86, 52.725,  3.02, 1.54, 0))
# 6731280
# [{'coin': 'ETCUSDT', 'side': -1, 'time': 6731280, 'last_price': 54.62, 'average_price': 54.183, 'volume': 1.25, 'leverage': 20, 'pnl': -18.71435690161113, 'profit': -0.6351249999999973, 'spec_pnl': -2.563163676309055, 'price': 54.69}, {'coin': 'ETCUSDT', 'side': 1, 'time': 6731280, 'last_price': 54.62, 'average_price': 54.62, 'volume': 0.62, 'leverage': 20, 'pnl': 2.563163676309055, 'profit': 0.04271800000000017, 'spec_pnl': 2.563163676309055, 'price': 54.69}]
# GOOD take short 1 6731340 [9900.0] 54.62
# order plus -0.6351249999999973
# 6731340
# order plus 0.04271800000000017
# 6933960
# [{'coin': 'ETCUSDT', 'side': 1, 'time': 6933960, 'last_price': 51.86, 'average_price': 52.725, 'volume': 3.02, 'leverage': 20, 'pnl': -29.397818871503027, 'profit': -2.3438219999999954, 'spec_pnl': 3.4708831469341854, 'price': 51.95}, {'coin': 'ETCUSDT', 'side': -1, 'time': 6933960, 'last_price': 51.86, 'average_price': 51.86, 'volume': 1.54, 'leverage': 20, 'pnl': -3.4708831469341845, 'profit': -0.14029400000000522, 'spec_pnl': -3.4708831469341845, 'price': 51.95}]
# GOOD take long 2 6934020 [51.4696] 51.86
# order plus -0.14029400000000522
# 6934020
# order plus -2.3438219999999954
# 6934020
