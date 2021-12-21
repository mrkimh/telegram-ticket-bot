import sqlite3
import os
from enum import Enum


def load_local_token():
    with open("./local_storage/token.txt", "r") as file:
        token = file.read()
    return token


def get_bot_token(var):
    return os.environ[var]


def establish_db_connection():
    connection = sqlite3.connect("./local_storage/db/telegram_bot.db")
    return connection


def generate_db_structure():
    connection = establish_db_connection()
    cursor = connection.cursor()
    with open("./db.sql", "r") as file:
        init_script = file.read()
        cursor.executescript(init_script)
    connection.commit()


def add_new_admin(tg_id: int):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"insert into admin_users (telegram_user_id) values ({tg_id});")
    connection.commit()
    return validate_admin(tg_id)


def validate_admin(tg_id: int):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"select * from ADMIN_USERS where telegram_user_id = {tg_id}")
    result = cursor.fetchall()
    return len(result) > 0


def get_categories():
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute("select * from categories")
    return cursor.fetchall()


def get_questions(category_id: int):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"select id,question,answer from questions where category={category_id}")
    return cursor.fetchall()


def user_exists(tg_id: int):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"select * from users where telegram_user_id = {tg_id}")
    result = cursor.fetchall()
    return len(result) > 0


def add_or_update_user(tg_id, tg_username, name=None, email=None, grade=None):
    if name is None:
        name = "NULL"
    if email is None:
        email = "NULL"
    if grade is None:
        grade = "NULL"
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT OR REPLACE into users (telegram_user_id, username, name, email, grade) values ({tg_id}, \"{tg_username}\", \"{name}\", \"{email}\", \"{grade}\")")
    connection.commit()


def get_user(tg_id):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"select * from users where telegram_user_id = {tg_id}")
    res = cursor.fetchone()
    return res


def remove_category(cat_id: int):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"delete from categories where id={cat_id}")
    connection.commit()


def add_category(name):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"insert into categories (category) values (\"{name}\")")
    connection.commit()


def remove_question(q_id):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"delete from questions where id={q_id}")
    connection.commit()


def add_question(cat_id, question, answer):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        f"insert into questions (category, question, answer) values ({cat_id}, \"{question}\", \"{answer}\")")
    connection.commit()


def get_active_tickets():
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute('select * from tickets where is_active=1')
    res = cursor.fetchall()
    return res


def close_ticket(u_id):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"select * from tickets where user={u_id} and is_active=1")
    cur_record = cursor.fetchone()
    if cur_record is not None:
        cursor.execute(
            f'insert or replace into tickets values ({cur_record[0]}, \"{cur_record[1]}\",  \"{cur_record[2]}\", 0)')
        connection.commit()


def has_active_ticket(u_id):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"select * from tickets where user={u_id} and is_active=1")
    res = cursor.fetchone()
    if res is not None:
        return True
    else:
        return False


def add_new_ticket(user_id, text):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"insert into tickets (user, content) values ({user_id}, \"{text}\")")
    connection.commit()
    cursor.execute(f"select id from tickets where user={user_id} and is_active=1")
    ticket_id = cursor.fetchone()[0]
    return ticket_id


def find_first_int(s: str):
    number = 0
    started = False
    for char in s:
        if char.isdigit():
            number = number * 10 + int(char)
            started = True
        elif started:
            break
    return number


def get_ticket_author(ticket_id):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"select user from tickets where id={ticket_id}")
    res = cursor.fetchone()[0]
    return res


class UserStatus(Enum):
    name = 1
    email = 2
    grade = 3
    fill_compl = 4
    adding_cat = 5
    adding_question = 6

