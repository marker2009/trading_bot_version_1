import time as tm

import mysql.connector

timm = tm.time()
from work_with_spartan import *

SERVER = input()


def delete(ok):
    try:
        cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                       host='quejutuni.beget.app',
                                       database='projectimperial')
        cursor1 = cnx1.cursor()
    except:
        try:
            send_error("error in mysql conn")
        except:
            print("very bad in send error")
    try:
        for i in ok:
            while True:
                try:
                    query1 = ("DELETE FROM `need` WHERE `id` = " + str(i))
                    cursor1.execute(query1)
                    cnx1.commit()
                    break
                except:
                    pass
    except:
        try:
            send_error("error in for in delete")
        except:
            print("very bad in send error")
    return None


def check_need_to_add():
    try:
        s_id = SERVER
        cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                       host='quejutuni.beget.app',
                                       database='projectimperial')
        cursor1 = cnx1.cursor()
        query1 = ("SELECT * from `need` WHERE `s_id` = " + str(s_id))
        cursor1.execute(query1)
        mas = []
        for i in cursor1:
            mas.append(i)
        return mas
    except:
        try:
            er = []
            try:
                return []
            except:
                er = "error in return []"
            send_error("errro in need_to_add" + str(er))
        except:
            print("very bad in send_error in need_to_add")


def send_time():
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("UPDATE `times` SET `tim` = " + str(tm.time()) + "WHERE `s_id` = " + SERVER)
    cursor1.execute(query1)
    cnx1.commit()



def get_coin(bot_id):
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("SELECT * from `bots` WHERE `id` = " + str(bot_id))
    cursor1.execute(query1)
    for i in cursor1:
        buf = json.loads(i[3].replace("\n", ""))
        return buf['coin']


clas = work_1(["A7hKrcISyhFZdzddCZ"], ["hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI"])
leverage = 20
# tks = [4, 4, 5, 6, 10]
tks = 1
mas_1 = [7, 8, 8, 8, 10]
mas_2 = mas_1[::]
summm = 2000
orders.summ = summm

col = 0
mi = 10 ** 1000
ds = []
ma = 0

flag = int(input())
if flag == 0:
    print("ok")
    import dill  # pip install dill --user

    filename = 'save.pkl'
    dill.load_session(filename)
else:
    print("ok")
    from pybit.unified_trading import HTTP

    session = HTTP(api_key="fofVie6eTCqLKyFhX8", api_secret="21WRLx2EsDVJad3duK2PbzxxRdhS4P3gK2yR")
    import dill

    clas = work_1(["A7hKrcISyhFZdzddCZ"], ["hBmMLMprHruxZL6QxTy35JpWsbBAR9234aWI"])
    ol = 0
    filename = 'save.pkl'
coins = ['LTCUSDT', "KSMUSDT"]
st = time.time()
while True:
    try:
        ol += 1
        # tt.sleep(1)
        data = {}
        for i in coins:
            buf = session.get_tickers(
                category="inverse",
                symbol=i,
            )['result']['list'][0]['lastPrice']
            data[i] = float(buf)
        print(data)
        clas.obxod(data)
        if ol % 10 == 0:
            try:
                dill.dump_session(filename)
            except:
                try:
                    send_error("error in save to dill")
                except:
                    print("very bad in send+_error")

        if ol % 10 == 0:
            try:
                buf = check_need_to_add()
            except:
                try:
                    send_error("error in check to add")
                except:
                    print("very_bad in send_error")
            ok = []
            for i in buf:
                try:
                    print(i)
                    clas.add_user("", "", "", 1, [], [], 0, 0, 0, 10, str(i[2]), 0, 0, 0, 0, [], [], data)
                    ok.append(i[0])
                except Exception as e:
                    try:
                        send_error("add user is error" + str(i[2]) + str(e))
                    except:
                        print("very_bad")
            try:
                delete(ok)
            except:
                try:
                    send_error("error in delete")
                except:
                    print("very bad in send error")
        try:
         if tm.time() - st > 20:

            st = tm.time()
            send_time()
        except:
            try:
                send_error("error in send_time")
            except:
                print("very bad in send error")

    except Exception as e:
        try:
            send_error("error in  main loop" + str(e))
        except:
            print("very bad in send error")
