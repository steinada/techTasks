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
sorting, query_where, sort_dict = '', '', {'director': 'd.name', 'title': 'f.name'}
sort_by = []
query = None
for param in sort_by:
    sorting += f", {sort_dict[param]}"
if query:
    query_where += f"WHERE f.name LIKE '%{query}%'"
db.execute(""" SELECT f.*, COUNT(DISTINCT(l.id)) AS likes
                    FROM film f
                    LEFT JOIN film_director fd ON fd.film_id = f.id
                    LEFT JOIN director d ON d.id = fd.director_id
                    LEFT JOIN film_genre fg ON fg.film_id = f.id
                    LEFT JOIN genre g ON g.id = fg.genre_id
                    LEFT JOIN film_mpa fm ON fm.film_id = f.id
                    LEFT JOIN mpa m ON m.id = fm.mpa_id
                    LEFT JOIN like l ON l.film_id = f.id
                    {query_where}
                    GROUP BY f.id, fd.id, fg.id
                    ORDER BY likes DESC {sorting} """.format(sorting=sorting, query_where=query_where))

a = db.fetchall()
connection.commit()
connection.close()
print(*a, sep='\n')
#
# user_one, user_two = 2, 1
# user_one, user_two = sorted(user_one, user_two)
# print(user_one, user_two)
