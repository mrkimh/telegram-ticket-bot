import sqlite3
from enum import Enum


def load_token():
    with open("./local_storage/token.txt", "r") as file:
        token = file.read()
    return token


def establish_db_connection():
    connection = sqlite3.connect("./local_storage/db/telegram_bot.db")
    return connection


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


def add_or_update_user(tg_id, name=None, email=None, grade=None):
    if name is None:
        name = "NULL"
    if email is None:
        email = "NULL"
    if grade is None:
        grade = "NULL"
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT OR REPLACE into users (telegram_user_id, name, email, grade) values ({tg_id}, \"{name}\", \"{email}\", \"{grade}\")")
    connection.commit()


def get_user(tg_id):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"select * from users where telegram_user_id = {tg_id}")
    res = cursor.fetchone()
    if len(res) > 0:
        return res
    else:
        return None


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
    cursor.execute(f"insert into questions (category, question, answer) values ({cat_id}, \"{question}\", \"{answer}\")")
    connection.commit()


def add_new_ticket(user_id):
    pass


class UserStatus(Enum):
    name = 1
    email = 2
    grade = 3
    fill_compl = 4
    adding_cat = 5
    adding_question = 6



