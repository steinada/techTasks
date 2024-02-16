import sqlite3


db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"


class UserRepository:
    @staticmethod
    def add_user(params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO
        user (email, login, name, birthday)
        VALUES (?, ?, ?, ?) """, params)
        id = db.lastrowid
        connection.commit()
        connection.close()
        return id

    @staticmethod
    def update_user(params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" UPDATE user
        SET email = ?, login = ?, name = ?, birthday = ?
        WHERE id = ?""", params)
        connection.commit()
        connection.close()

    @staticmethod
    def get_users():
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM user """)
        users = db.fetchall()
        connection.close()
        return users

    @staticmethod
    def get_created_users():
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT id FROM user """)
        user_ids = db.fetchall()
        connection.close()
        return user_ids

