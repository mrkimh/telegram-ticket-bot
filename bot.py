import telebot
from utils import *
import logging

bot = telebot.TeleBot(load_token())
context = dict()


@bot.message_handler(commands=['start', 'help', 'info'])
def process_start_command(message):
    if not user_exists(message.chat.id):
        add_or_update_user(message.chat.id)
    bot.send_message(message.chat.id, "hello")
    info_markup = telebot.types.InlineKeyboardMarkup()
    info_markup.add(telebot.types.InlineKeyboardButton(text="Заполнить анкету", callback_data="user_info accept"))
    info_markup.add(telebot.types.InlineKeyboardButton(text="Отказаться", callback_data="user_info decline"))
    bot.send_message(message.chat.id, "Для более эффективного взаимодействия с ботом рекомендуется заполнить основную "
                                      "информацию о себе", reply_markup=info_markup)


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


@bot.message_handler(commands=['faq'])
def process_faq_command(message: telebot.types.Message):
    categories = get_categories()
    categories_markup = telebot.types.InlineKeyboardMarkup()
    for category in categories:
        categories_markup.add(telebot.types.InlineKeyboardButton(text=f"{category[0]}. {category[1]}",
                                                                 callback_data=f"faq {category[0]}"))
    bot.send_message(message.chat.id, "Разделы:", reply_markup=categories_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: telebot.types.CallbackQuery):
    if call.message and call.data:
        if call.data.split()[0] == "faq":
            questions = get_questions(int(call.data.split()[1]))
            reply = ""
            for q in questions:
                reply += f"{q[0]}. {q[1]}\n {q[2]}\n\n"
            bot.send_message(call.message.chat.id, reply)
        if call.data.split()[0] == "user_info":
            if call.data.split()[1] == "decline":
                bot.send_message(call.message.chat.id, "Вы в любое время можете заполнить или изменить анкету. "
                                                       "Для этого используйте команду /info")
            elif call.data.split()[1] == "accept":
                context[call.from_user.id] = UserStatus.name
                fill_user_info(call.from_user.id)
        if call.data.split()[0] == "skip":
            if call.data.split()[1] == "name" and context.get(call.message.chat.id) == UserStatus.name:
                context.pop(call.message.chat.id)
                context[call.message.chat.id] = UserStatus.email
                fill_user_info(call.message.chat.id)
            elif call.data.split()[1] == "email" and context.get(call.message.chat.id) == UserStatus.email:
                context.pop(call.message.chat.id)
                context[call.message.chat.id] = UserStatus.grade
                fill_user_info(call.message.chat.id)
            elif call.data.split()[1] == "grade" and context.get(call.message.chat.id) == UserStatus.grade:
                context.pop(call.message.chat.id)
                context[call.message.chat.id] = UserStatus.fill_compl
                fill_user_info(call.message.chat.id)


def fill_user_info(user):
    status = context[user]
    if status == UserStatus.name:
        name_markup = telebot.types.InlineKeyboardMarkup()
        name_markup.add(telebot.types.InlineKeyboardButton(text="Пропустить", callback_data="skip name"))
        bot.send_message(user, "Ваше имя?", reply_markup=name_markup)
    elif status == UserStatus.email:
        email_markup = telebot.types.InlineKeyboardMarkup()
        email_markup.add(telebot.types.InlineKeyboardButton(text="Пропустить", callback_data="skip email"))
        bot.send_message(user, "Ваш Email?", reply_markup=email_markup)
    elif status == UserStatus.grade:
        grade_markup = telebot.types.InlineKeyboardMarkup()
        grade_markup.add(telebot.types.InlineKeyboardButton(text="Пропустить", callback_data="skip grade"))
        bot.send_message(user, "Ваш класс?", reply_markup=grade_markup)
    elif status == UserStatus.fill_compl:
        context.pop(user)
        bot.send_message(user, "Спасибо! Информация сохранена. Вы можете обновить ее в любое время при помощи команды "
                               "/info")


@bot.message_handler(func=lambda message: True)
def process_message(message: telebot.types.Message):
    if not context.get(message.chat.id) is None:
        user, name, email, grade = get_user(message.chat.id)
        if context.get(message.chat.id) == UserStatus.name:
            name = message.text
            add_or_update_user(user, name, email, grade)
            context.pop(user)
            context[user] = UserStatus.email
            fill_user_info(user)
        elif context.get(message.chat.id) == UserStatus.email:
            email = message.text
            add_or_update_user(user, name, email, grade)
            context.pop(user)
            context[user] = UserStatus.grade
            fill_user_info(user)
        elif context.get(message.chat.id) == UserStatus.grade:
            grade = message.text
            add_or_update_user(user, name, email, grade)
            context.pop(user)
            context[user] = UserStatus.fill_compl
            fill_user_info(user)

    if message.chat.type == "private" and message.text.find("?") > 0 and not validate_admin(message.chat.id):
        process_new_ticket(message)


def process_new_ticket(message: telebot.types.Message):
    pass


bot.infinity_polling()
