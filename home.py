import json

import mysql.connector

cnx = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                              host='quejutuni.beget.app',
                              database='projectimperial')
cursor = cnx.cursor()
query = ("SELECT * from `bots` WHERE `id` = 1")
cursor.execute(query)


def get_api(bot_id):
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("SELECT * from `apis` WHERE `id` = " + str(bot_id))
    cursor1.execute(query1)
    for i in cursor1:
        return i[2], i[3]


def is_work(bot_id):
    cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                   host='quejutuni.beget.app',
                                   database='projectimperial')
    cursor1 = cnx1.cursor()
    query1 = ("SELECT * from `bots` WHERE `id` = " + str(bot_id))
    cursor1.execute(query1)
    for i in cursor1:
        return i[2] == 1


print(is_work(1))
for i in cursor:
    buf = json.loads(i[3].replace("\n", ""))
    token = str(i[0])
    api, api_secret = get_api(i[0])
    layers_short = [i * buf['leverage'] for i in buf['short_layers']]
    layers_long = [i * buf['leverage'] for i in buf['long_layers']]
    multiplicity = 2
    delta_time = buf['time']
    leverage = buf['leverage']
    coin = buf['coin']
    unnormal_move = buf['pump'] * buf['leverage']
    take = buf['take'] * buf['leverage']
    stop = buf['stop'] * buf['leverage']
    print(token, api, api_secret, layers_long, layers_short, multiplicity, delta_time, leverage, coin, unnormal_move,
          take, stop)

cursor.close()
cnx.close()
