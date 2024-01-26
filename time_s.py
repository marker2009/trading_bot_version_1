import time
import time as tt
class times:
    def __init__(self, time):
        self.tim = time
    def time(self):
        return self.tim
    def change_time(self, time):
        self.tim = time
    def add_time(self, tim):
        self.tim += tim

class orde:
    def __init__(self):
        self.file = open("output.txt", "w")
        self.files = open("takesorstops.txt", "w")
        self.order =[]
        self.summ = 1000
        self.oun = 0
        self.volume = 0
    def add_volume(self, x):
        self.volume += x
    def add_take_or_stop(self, st):
        self.files.write(st + " " + str(time.time()) +"\n")
    def append(self, data):
        self.order.append(data + [time.time()])
    def update_summ(self, data):
        self.file.write("order_plus" + " " + str(data) + " " + str(time.time()) + "\n")
        print("order plus", data)
        print(time.time())
        self.summ += data

time = times(0)
orders = orde()
