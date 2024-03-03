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

    def add_friend(self, user_one, user_two, status):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO friend (user_one, user_two, status)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_one, user_two) DO UPDATE SET
                    status = CASE
                        WHEN excluded.status = 3 - friend.status THEN 3
                        WHEN friend.status = 3 THEN friend.status
                        ELSE excluded.status
                    END """, (user_one, user_two, status))
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
                    WHERE (user_one = {id} AND status IN (1, 3) OR user_two = {id} AND status IN (2, 3))
                    AND u.id = ids """.format(id=id))
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

    def get_common_friends(self, user_one, user_two):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT u.*, CASE f_one.user_one
                    WHEN {id_one} THEN f_one.user_two
                    ELSE f_one.user_one
                    END ids_f_one,
                    CASE f_two.user_one
                    WHEN {id_two} THEN f_two.user_two
                    ELSE f_two.user_one
                    END ids_f_two
                    FROM friend f_one, friend f_two, user u
                    WHERE (f_one.user_one = {id_one} AND f_one.status IN (1, 3)
                        OR f_one.user_two = {id_one} AND f_one.status IN (2, 3))
                    AND (f_two.user_one = {id_two} AND f_two.status IN (1, 3)
                        OR f_two.user_two = {id_two} AND f_two.status IN (2, 3))
                    AND u.id = ids_f_one
                    AND ids_f_one = ids_f_two """.format(id_one=user_one, id_two=user_two))
        common_friends = db.fetchall()
        connection.close()
        return common_friends
