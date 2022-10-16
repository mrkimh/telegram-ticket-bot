import telebot
from utils import *
import logging

bot = telebot.TeleBot(get_bot_token('5711490877:AAHCU5uKeFXREXZrFCZlNsUX_5UVBBH1XTQ'))
context = dict()
main_chat_id = get_main_chat()


@bot.message_handler(commands=['start', 'help', 'info'])
def process_start_command(message: telebot.types.Message):
    if not user_exists(message.chat.id):
        add_or_update_user(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, "hello")
    info_markup = telebot.types.InlineKeyboardMarkup()
    info_markup.add(telebot.types.InlineKeyboardButton(text="Заполнить анкету", callback_data="user_info accept"))
    info_markup.add(telebot.types.InlineKeyboardButton(text="Отказаться", callback_data="user_info decline"))
    bot.send_message(message.chat.id, "Для более эффективного взаимодействия с ботом рекомендуется заполнить основную "
                                      "информацию о себе", reply_markup=info_markup)


@bot.message_handler(commands=['id'])
def process_start_command(message: telebot.types.Message):
    bot.send_message(message.chat.id, message.chat.id)


@bot.message_handler(commands=['addfirstadmin'])
def process_afa_command(message: telebot.types.Message):
    try:
        if not validate_admin(message.from_user.id):
            add_new_admin(message.from_user.id)
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
                if validate_admin(message.from_user.id):
                    add_new_admin(int(words[1]))
                    bot.send_message(message.chat.id, "Админ успешно добавлен")
            except Exception as e:
                bot.reply_to(message, "error")
                print(e)
    else:
        bot.send_message(message.chat.id, "Недостаточно прав")


@bot.message_handler(commands=['removecategory'])
def process_remove_category_command(message: telebot.types.Message):
    if validate_admin(message.from_user.id):
        categories = get_categories()
        categories_markup = telebot.types.InlineKeyboardMarkup()
        i = 0
        for category in categories:
            i += 1
            categories_markup.add(telebot.types.InlineKeyboardButton(text=f"{i}. {category[1]}",
                                                                     callback_data=f"remove {category[0]}"))
        bot.send_message(message.chat.id, "Выберите категорию для удаления", reply_markup=categories_markup)
    else:
        bot.send_message(message.chat.id, "Недостаточно прав")


@bot.message_handler(commands=['tickets'])
def get_all_active_tickets_command(message: telebot.types.Message):
    if validate_admin(message.from_user.id):
        tickets = get_active_tickets()
        for ticket in tickets:
            u_name = get_user(ticket[1])[4]
            bot.send_message(message.chat.id,
                             f"Ticket  ID {ticket[0]}\nFrom user {ticket[1]} @{u_name}\nText: {ticket[2]}")
    else:
        bot.send_message(message.chat.id, "Недостаточно прав")


@bot.message_handler(commands=['close'])
def process_close_ticket_command(message: telebot.types.Message):
    if validate_admin(message.from_user.id):
        user_id = message.text.split()[1]
        close_ticket(user_id)
        bot.send_message(message.chat.id, "Ticket помечен как завершенный")
    else:
        close_ticket(message.from_user.id)
        if not has_active_ticket(message.from_user.id):
            bot.send_message(message.chat.id, "У вас больше нет открытых запросов.")


@bot.message_handler(commands=['addcategory'])
def process_add_category_command(message: telebot.types.Message):
    if validate_admin(message.from_user.id):
        context[message.from_user.id] = UserStatus.adding_cat
        bot.send_message(message.chat.id, "Введите название категории")
    else:
        bot.send_message(message.chat.id, "Недостаточно прав")


@bot.message_handler(commands=['removequestion'])
def process_remove_question_command(message: telebot.types.Message):
    if validate_admin(message.from_user.id):
        categories = get_categories()
        categories_markup = telebot.types.InlineKeyboardMarkup()
        i = 0
        for category in categories:
            i += 1
            categories_markup.add(telebot.types.InlineKeyboardButton(text=f"{i}. {category[1]}",
                                                                     callback_data=f"rm_question_cat {category[0]}"))
        bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=categories_markup)
    else:
        bot.send_message(message.chat.id, "Недостаточно прав")


@bot.message_handler(commands=['addquestion'])
def process_add_question_command(message: telebot.types.Message):
    if validate_admin(message.from_user.id):
        categories = get_categories()
        categories_markup = telebot.types.InlineKeyboardMarkup()
        i = 0
        for category in categories:
            i += 1
            categories_markup.add(telebot.types.InlineKeyboardButton(text=f"{i}. {category[1]}",
                                                                     callback_data=f"add_question {category[0]}"))
        bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=categories_markup)
    else:
        bot.send_message(message.chat.id, "Недостаточно прав")


@bot.message_handler(commands=['getinfo'])
def process_add_question_command(message: telebot.types.Message):
    if validate_admin(message.from_user.id):
        user = get_user(message.text.split()[1])
        if user is not None:
            bot.send_message(message.chat.id, f"User: @{user[4]}\nName: {user[1]}\nEmail: {user[2]}\nGrade: {user[3]}")
        else:
            bot.send_message(message.chat.id, "Uses does not exist.")
    else:
        bot.send_message(message.chat.id, "Недостаточно прав")


@bot.message_handler(commands=['faq'])
def process_faq_command(message: telebot.types.Message):
    categories = get_categories()
    categories_markup = telebot.types.InlineKeyboardMarkup()
    i = 0
    for category in categories:
        i += 1
        categories_markup.add(telebot.types.InlineKeyboardButton(text=f"{i}. {category[1]}",
                                                                 callback_data=f"faq {category[0]}"))
    bot.send_message(message.chat.id, "Разделы:", reply_markup=categories_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: telebot.types.CallbackQuery):
    if call.message and call.data:
        if call.data.split()[0] == "faq":
            questions = get_questions(int(call.data.split()[1]))
            reply = ""
            i = 1
            for q in questions:
                reply += f"{i}. {q[1]}\n{q[2]}\n\n"
                i += 1
            bot.send_message(call.message.chat.id, reply)
        elif call.data.split()[0] == "user_info":
            if call.data.split()[1] == "decline":
                bot.send_message(call.message.chat.id, "Вы в любое время можете заполнить или изменить анкету. "
                                                       "Для этого используйте команду /info")
            elif call.data.split()[1] == "accept":
                context[call.from_user.id] = UserStatus.name
                fill_user_info(call.from_user.id)
        elif call.data.split()[0] == "skip":
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
        elif call.data.split()[0] == "remove":
            cat_id = int(call.data.split()[1])
            remove_category(cat_id)
            bot.send_message(call.message.chat.id, "Категория успешно удалена")
        elif call.data.split()[0] == "rm_question_cat":
            questions = get_questions(int(call.data.split()[1]))
            questions_markup = telebot.types.InlineKeyboardMarkup()
            for q in questions:
                questions_markup.add(telebot.types.InlineKeyboardButton(text=f"{q[0]}. {q[2]}",
                                                                        callback_data=f"rm_question {q[0]}"))
            bot.send_message(call.message.chat.id, "Выберите вопрос для удаления", reply_markup=questions_markup)
        elif call.data.split()[0] == "rm_question":
            remove_question(call.data.split()[1])
            bot.send_message(call.message.chat.id, "Успешно удалено")
        elif call.data.split()[0] == "add_question":
            context[call.message.chat.id] = [UserStatus.adding_question, call.data.split()[1]]
            bot.send_message(call.message.chat.id, "Введите вопрос.")


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
    if not context.get(message.from_user.id) is None:
        if context.get(message.from_user.id) == UserStatus.name:
            user, name, email, grade, username = get_user(message.from_user.id)
            name = message.text
            add_or_update_user(user, username, name, email, grade)
            context.pop(user)
            context[user] = UserStatus.email
            fill_user_info(user)
        elif context.get(message.from_user.id) == UserStatus.email:
            user, name, email, grade, username = get_user(message.from_user.id)
            email = message.text
            add_or_update_user(user, username, name, email, grade)
            context.pop(user)
            context[user] = UserStatus.grade
            fill_user_info(user)
        elif context.get(message.from_user.id) == UserStatus.grade:
            user, name, email, grade, username = get_user(message.from_user.id)
            grade = message.text
            add_or_update_user(user, username, name, email, grade)
            context.pop(user)
            context[user] = UserStatus.fill_compl
            fill_user_info(user)
        elif context.get(message.from_user.id) == UserStatus.adding_cat:
            add_category(message.text)
            context.pop(message.from_user.id)
            bot.send_message(message.from_user.id, f"Категория успешно добавлена")
        elif context.get(message.from_user.id).__class__ is list:
            ls = context.get(message.from_user.id)
            if len(ls) == 2:
                context.pop(message.from_user.id)
                ls.append(message.text)
                context[message.chat.id] = ls
                bot.send_message(message.chat.id, "Введите ответ на вопрос")
            elif len(ls) == 3:
                context.pop(message.from_user.id)
                cat_id = ls[1]
                question = ls[2]
                ans = message.text
                add_question(cat_id, question, ans)
                bot.send_message(message.chat.id, "Вопрос успешно добавлен!")

    elif message.chat.type == "private" and not validate_admin(message.chat.id):
        if not has_active_ticket(message.from_user.id):
            ticket_id = add_new_ticket(message.from_user.id, message.text)
            bot.send_message(message.chat.id, "Запрос отправлен.")
            bot.send_message(main_chat_id,
                             f"New Ticket  ID {ticket_id}\nFrom user {message.from_user.id} @{message.from_user.username}"
                             f"\nContent: {message.text}")
        else:
            if message.reply_to_message is not None and validate_admin(message.reply_to_message.forward_from.id):
                print(message.reply_to_message)
                bot.forward_message(main_chat_id, message.chat.id, message.id)
                bot.send_message(message.chat.id, "Отправлено")
            else:
                bot.send_message(message.chat.id, "У вас есть незавершенный запрос. Если вы хотите отправить новый "
                                                  "запрос, завершите уже открытый при помощи команды /close.")
    elif validate_admin(message.from_user.id) and message.reply_to_message is not None \
            and message.chat.type != "private":
        if message.reply_to_message.text.find("Ticket  ID") >= 0:
            ticket_id_to_reply = find_first_int(message.reply_to_message.text)
            user = get_ticket_author(ticket_id_to_reply)
            bot.forward_message(user, message.chat.id, message.id)


bot.infinity_polling()
