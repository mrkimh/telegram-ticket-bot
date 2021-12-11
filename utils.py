import sqlite3


def load_token():
    with open("./local_storage/token.txt", "r") as file:
        token = file.read()
    return token


def add_first_admin_command():
    with open("./local_storage/add_first_admin_command.txt", "r") as file:
        command = file.read()
    return command


def add_new_admin(tg_id: int):
    connection = establish_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"insert into admin_users (telegram_user_id) values ({tg_id});")
    connection.commit()
    return validate_admin(tg_id)


def validate_admin(tg_id: int):
    connection = establish_db_connection()
    cursor = establish_db_connection().cursor()
    cursor.execute(f"select * from ADMIN_USERS where telegram_user_id = {tg_id}")
    result = cursor.fetchall()
    return len(result) > 0


def establish_db_connection():
    connection = sqlite3.connect("./local_storage/db/telegram_bot.db")
    return connection


# con = establish_db_connection()
# cur = con.cursor()
# cur.execute(f"insert into admin_users (telegram_user_id) values (55555555);")
# con.commit()


