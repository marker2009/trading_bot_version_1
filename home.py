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
print(get_res(37.38, 37.64, 0.06, 0.03, 0))
# print(al(76026 * 1.01, pr, apr,v1, v2))
