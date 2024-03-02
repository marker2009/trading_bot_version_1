import json
import time
import time as tm

import mysql.connector
import string
import random
port = 22

def chose_server(type):
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("SELECT * from `servers` WHERE `type` = " + str(type))
    cursor1.execute(query1)
    mas = [i for i in cursor1]
    min_users_server = min(mas, key = lambda x:x[1]) if len(mas) != 0 else []
    return min_users_server
def choose_glav_server():
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("SELECT * from `glav_servers`")
    cursor1.execute(query1)
    mas = [i for i in cursor1]
    if len(mas)!=0:
        min_users_server = min(mas , key = lambda x:x[6])
    else:
        min_users_server = []
    return min_users_server
def add_server(type,id):
    return True
def is_work():
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("SELECT * from `balance`")
    cursor1.execute(query1)
    mas = []
    for i in cursor1:
        mas.append(i)
def work(type, bot_id):
    buf = chose_server(type)
    if buf == [] or buf[1] >= buf[6]:
        bufs = choose_glav_server()
        cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
        cursor1 = cnx1.cursor()
        query1 = ("INSERT INTO `servers`  (`type`, `ip`, `glav_server`) VALUES ('"+ str(type)  +"', '" + str(bufs[4]) + "', '" + str(bufs[0]) + "')")
        print(query1)
        cursor1.execute(query1)
        cnx1.commit()
        bus = cursor1.lastrowid
        add_server(type, bus)
    buf = chose_server(type)
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("INSERT INTO `need`  (`bot_id`, `s_id`) VALUES ('"+ str(bot_id) + "', '"+str(buf[0]) + "')")
    print(query1)
    cursor1.execute(query1)
    cnx1.commit()

# while True:
#     is_work()
#     time.sleep(1)
work(1, 1)
