import telebot
from utils import *
import logging

bot = telebot.TeleBot(load_token())


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.send_message(message.chat.id, "hello")


bot.infinity_polling()
