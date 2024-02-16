import sqlite3


connection = sqlite3.connect("../../filmorate.db")
db = connection.cursor()

db.execute(""" DROP TABLE user """)
db.execute(""" DROP TABLE film """)
db.execute(""" DROP TABLE rate """)

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

connection.commit()
connection.close()
