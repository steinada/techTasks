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
#                                 FOREIGN KEY (user_two) REFERENCES user(id),
#                                 UNIQUE(user_one,user_two))
#                                 """)
#
# db.execute(""" INSERT INTO friend
#             (user_one, user_two, status)
#              VALUES (?, ?, ?)
#              ON CONFLICT DO UPDATE SET status = 2""", (1, 2, 1))
db.execute(""" INSERT INTO friend
            (user_one, user_two, status)
             VALUES (?, ?, ?)
             ON CONFLICT DO UPDATE SET status = 2""", (1, 2, 1))
# db.execute(""" INSERT INTO friend
#             (user_one, user_two, status)
#              VALUES (?, ?, ?) """, (1, 2, 2))

db.execute(""" SELECT u.*, CASE user_one
                    WHEN {id} THEN user_two
                    ELSE user_one
                    END ids
                    FROM friend, user u
                    WHERE (user_one = {id} OR user_two = {id} AND status = 2) AND u.id = ids """.format(id=1))

a = db.fetchall()
connection.commit()
connection.close()
print(a)

user_one, user_two = 2, 1
user_one, user_two = sorted(user_one, user_two)
print(user_one, user_two)
