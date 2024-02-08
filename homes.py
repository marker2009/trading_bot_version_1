col = 0
for i in range(1, 30000):
    s = 5 * (i // 10)
    if s + 28 * 5 < 300 and s + 28 * 6 >= 300:
        col += 1
print(col)
