import json
import time as tm

import mysql.connector
import telebot
import string
import random
PASS = "dcefgxeahi"
bot_telebot = telebot.TeleBot('6409601467:AAHrQlILMfGXruvbkd4X6-woosxZzsRgY44')
for_pas = [chr(ord('a') + i) for i in range(26)] + ['/', '!', '@', '#', '$'] + [ str(i) for i in range(10)]
print(for_pas)
for_pas = for_pas * 5
s_bot = 1
def step2(message):
    s_bot = int(message.text)
    if s_bot not in [1,2,3]:
        bot_telebot.register_next_step_handler(bot_telebot.send_message(message.chat_id, "Некоректный тип бота, введите корретный"), step2)
    else:
        bot_telebot.register_next_step_handler(bot_telebot.send_message(message.chat.id, "Введите почту пользователя"), step3)
def step3(message):
     random.shuffle(for_pas)
     buf = "".join(for_pas[:10])
     cnx1 = mysql.connector.connect(user='projectimperial', password='L{=yHJ9+j?%tyJT$',
                                       host='quejutuni.beget.app',
                                       database='projectimperial')
     cursor1 = cnx1.cursor()
     query1 = ('INSERT INTO `bots` (`type`, `is_work`, `params`) VALUES (' + str(s_bot) + " , 0, '" + json.dumps({'type':1})+"')")
     print(query1)
     cursor1.execute(query1)
     cnx1.commit()
     bufs = cursor1.lastrowid
     print(bufs)
     query1 = ('INSERT INTO `users` (`mail`, `password`, `id_bot`) VALUES ("' +str(message.text) + '" , "'+str(buf)+'", '+str(bufs) + ')')
     print(query1)
     cursor1.execute(query1)
     cnx1.commit()
     bufs1 = cursor1.lastrowid
     query1 = ('INSERT INTO `apis` (`id`, `user_id`) VALUES (' + str(bufs) + " , " + str(bufs1) + ")")
     print(query1)
     cursor1.execute(query1)
     cnx1.commit()

     bot_telebot.send_message(message.chat.id, "Пользователь успешно добавлен\nmail: "+  message.text+  " \npassword:" +  buf)


@bot_telebot.message_handler(commands=['adduser'])
def add(message):
    if message.from_user.id in admin:
        bot_telebot.register_next_step_handler(bot_telebot.send_message(message.chat.id, 'Введите номер бота'),step2)
        print("1")

admin = []
def check_id(message):
    global is_prosh, ids
    if message.text == PASS:
        bot_telebot.send_message(message.chat.id, "вы прошли проверку")
        admin.append(message.from_user.id)
    else:
        bot_telebot.send_message(message.chat.id, "Вы не прошли проверку")

@bot_telebot.message_handler(commands=['start'])
def start(message):
    chat = message.chat.id
    bot_telebot.register_next_step_handler(bot_telebot.send_message(chat, 'Здравствуйте, введите код админа'), check_id)

bot_telebot.polling(none_stop=True)

