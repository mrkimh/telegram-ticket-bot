import telebot
from utils import *
import logging

bot = telebot.TeleBot(load_token())


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.send_message(message.chat.id, "hello")


@bot.message_handler(commands=['id'])
def process_start_command(message: telebot.types.Message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id, message.chat.id)


@bot.message_handler(commands=[f'{add_first_admin_command()}'])
def process_afa_command(message: telebot.types.Message):
    try:
        add_new_admin(message.chat.id)
        bot.reply_to(message, "Вы успешно получили админ права")
    except Exception as e:
        bot.reply_to(message, "error")
        print(e)


@bot.message_handler(commands=['addadmin'])
def process_add_admin_command(message: telebot.types.Message):
    if validate_admin(message.from_user.id):
        words = message.text.split()
        if len(words) == 2 and words[1].isnumeric():
            try:
                add_new_admin(int(words[1]))
                bot.send_message(message.chat.id, "Админ успешно добавлен")
            except Exception as e:
                bot.reply_to(message, "error")
                print(e)
    else:
        bot.send_message(message.chat.id, "Недостаточно прав")


bot.infinity_polling()
