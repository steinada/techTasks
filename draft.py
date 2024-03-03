import sqlite3


db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"
connection = sqlite3.connect(db_path, check_same_thread=False)
db = connection.cursor()
# db.execute(""" DROP TABLE friend """)
# db.execute(""" CREATE TABLE IF NOT EXISTS friend (
#                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                 user_one INTEGER,
#                                 user_two INTEGER,
#                                 status INTEGER,
#                                 FOREIGN KEY (user_one) REFERENCES user(id),
#                                 FOREIGN KEY (user_two) REFERENCES user(id))
#                                 """)
#
# db.execute(""" INSERT INTO friend
#             (user_one, user_two, status)
#              VALUES (?, ?, ?)""", (1, 3, 2))
# db.execute(""" INSERT INTO friend
#             (user_one, user_two, status)
#              VALUES (?, ?, ?)""", (1, 3, 1))
# db.execute(""" INSERT INTO friend
#             (user_one, user_two, status)
#              VALUES (?, ?, ?)""", (2, 3, 2))
# db.execute(""" INSERT INTO friend
#             (user_one, user_two, status)
#              VALUES (?, ?, ?)""", (2, 1, 1))

db.execute(""" SELECT u.*, CASE user_one
                    WHEN {id} THEN user_two
                    ELSE user_one
                    END ids
                    FROM friend, user u
                    WHERE (user_one = {id} AND status IN (2, 3) OR user_two = {id} AND status IN (1, 3))
                    AND u.id = ids """.format(id=1))
a1 = db.fetchall()
db.execute(""" SELECT u.*, CASE user_one
                    WHEN {id} THEN user_two
                    ELSE user_one
                    END ids
                    FROM friend, user u
                    WHERE (user_one = {id} AND status IN (2, 3) OR user_two = {id} AND status IN (1, 3))
                    AND u.id = ids """.format(id=2))
a2 = db.fetchall()
db.execute(""" SELECT u.*, CASE f.user_one
                    WHEN {id} THEN f.user_two
                    ELSE f.user_one
                    END ids1,
                    CASE ff.user_one
                    WHEN {idd} THEN ff.user_two
                    ELSE ff.user_one
                    END ids2
                    FROM friend f, friend ff, user u
                    WHERE (f.user_one = {id} AND f.status IN (2, 3) OR f.user_two = {id} AND f.status IN (1, 3))
                    AND (ff.user_one = {idd} AND ff.status IN (2, 3) OR ff.user_two = {idd} AND ff.status IN (1, 3))
                    AND u.id = ids1
                    AND ids1 = ids2 """.format(id=1, idd=2))

a = db.fetchall()
connection.commit()
connection.close()
print(a1)
print(a2)
print(a)
#
# user_one, user_two = 2, 1
# user_one, user_two = sorted(user_one, user_two)
# print(user_one, user_two)
