import sqlite3


db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"


class UserRepository:
    def add_user(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO
        user (email, login, name, birthday)
        VALUES (?, ?, ?, ?) """, params)
        id = db.lastrowid
        connection.commit()
        connection.close()
        return id

    def update_user(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" UPDATE user
        SET email = ?, login = ?, name = ?, birthday = ?
        WHERE id = ?""", params)
        connection.commit()
        connection.close()

    def get_users(self):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM user """)
        users = db.fetchall()
        connection.close()
        return users

    @classmethod
    def get_created_users(cls):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT id FROM user """)
        user_ids = db.fetchall()
        connection.close()
        return user_ids

    def add_friend(self, user_one, user_two):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO friend
                    (user_one, user_two)
                     VALUES (?, ?) """, (user_one, user_two))
        connection.commit()
        connection.close()

    def delete_friend(self, user_one, user_two):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" DELETE FROM friend
                    WHERE user_one = ? AND user_two = ?
                    OR user_one = ? AND user_two = ? """,
                   (user_one, user_two, user_two, user_one))
        connection.commit()
        connection.close()

    def get_friends_of_user(self, id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT u.*, CASE user_one
                    WHEN {id} THEN user_two
                    ELSE user_one
                    END ids
                    FROM friend, user u
                    WHERE (user_one = {id} OR user_two = {id}) AND u.id = ids """.format(id=id))
        friends = db.fetchall()
        connection.close()
        return friends

    def get_user_by_id(self, id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM user WHERE id = {id} """.format(id=id))
        user = db.fetchall()
        connection.close()
        return user
