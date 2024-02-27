import sqlite3


connection = sqlite3.connect("../../filmorate.db")
db = connection.cursor()

db.execute(""" DROP TABLE user """)
db.execute(""" DROP TABLE film """)
db.execute(""" DROP TABLE rate """)
db.execute(""" DROP TABLE like """)
db.execute(""" DROP TABLE friend """)
db.execute(""" DROP TABLE genre """)
db.execute(""" DROP TABLE mpa """)
db.execute(""" DROP TABLE film_genre """)
db.execute(""" DROP TABLE film_mpa """)


db.execute(""" CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                email VARCHAR,
                                login VARCHAR,
                                name VARCHAR,
                                birthday DATE
                                ) """)

db.execute(""" CREATE TABLE IF NOT EXISTS film (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR,
                                description VARCHAR,
                                release_date DATE,
                                duration INTEGER
                                ) """)

db.execute(""" CREATE TABLE IF NOT EXISTS rate (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                rate INTEGER,
                                film_id INTEGER,
                                FOREIGN KEY (film_id) REFERENCES film(id))
                                """)

db.execute(""" CREATE TABLE IF NOT EXISTS friend (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_one INTEGER,
                                user_two INTEGER,
                                status INTEGER,
                                FOREIGN KEY (user_one) REFERENCES user(id),
                                FOREIGN KEY (user_two) REFERENCES user(id),
                                UNIQUE(user_one,user_two))
                                """)

db.execute(""" CREATE TABLE IF NOT EXISTS like (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                film_id INTEGER,
                                FOREIGN KEY (film_id) REFERENCES film(id),
                                FOREIGN KEY (user_id) REFERENCES user(id))
                                """)
db.execute(""" CREATE TABLE IF NOT EXISTS genre (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR)
                                """)
db.execute(""" CREATE TABLE IF NOT EXISTS mpa (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR)
                                """)

db.execute(""" CREATE TABLE IF NOT EXISTS film_genre (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                genre_id INTEGER,
                                film_id INTEGER,
                                FOREIGN KEY (film_id) REFERENCES film(id))
                                """)
db.execute(""" CREATE TABLE IF NOT EXISTS film_mpa (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                mpa_id INTEGER,
                                film_id INTEGER,
                                FOREIGN KEY (film_id) REFERENCES film(id))
                                """)

db.execute(""" INSERT INTO genre (name)
            VALUES ('Комедия'), ('Драма'), ('Мультфильм'), ('Триллер'), ('Документальный'), ('Боевик') """)

db.execute(""" INSERT INTO mpa (name)
            VALUES ('G'), ('PG'), ('PG-13'), ('R'), ('NC-17') """)


connection.commit()
connection.close()
