CREATE TABLE IF NOT EXISTS admin_users (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_user_id BIGINT  UNIQUE
                             NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
    telegram_user_id BIGINT PRIMARY KEY,
    name             STRING,
    email            STRING,
    grade            STRING
);


CREATE TABLE IF NOT EXISTS tickets (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user      BIGINT  REFERENCES users (telegram_user_id) ON DELETE CASCADE
                                                          ON UPDATE CASCADE
                      NOT NULL,
    content   STRING,
    is_active BOOLEAN DEFAULT (true) 
                      NOT NULL
);


CREATE TABLE IF NOT EXISTS categories (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    category STRING  NOT NULL
                     UNIQUE
);


CREATE TABLE IF NOT EXISTS questions (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    category INTEGER REFERENCES categories (id) ON DELETE CASCADE
                                                ON UPDATE CASCADE,
    question STRING  NOT NULL,
    answer   STRING  NOT NULL
);
