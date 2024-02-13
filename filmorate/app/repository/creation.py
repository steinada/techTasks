import sqlite3


connection = sqlite3.connect("filmorate.db")
db = connection.cursor()

db.execute(""" CREATE TABLE user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                email VARCHAR,
                                login VARCHAR,
                                name VARCHAR,
                                birthday DATE
                                ) """)

db.execute(""" CREATE TABLE film (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR,
                                description VARCHAR,
                                release_date DATE,
                                duration INTEGER
                                ) """)

connection.commit()
connection.close()
