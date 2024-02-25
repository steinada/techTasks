# import sqlite3
#
#
# db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"
# connection = sqlite3.connect(db_path, check_same_thread=False)
# db = connection.cursor()
# aa = [1, 2]
# ids = str(aa).strip("[]")
# db.execute(""" SELECT fm.film_id, fm.mpa_id, m.name
#                     FROM film_mpa fm, mpa m
#                     WHERE fm.film_id IN ({ids}) AND m.id = fm.mpa_id """.format(ids=ids))
# a = db.fetchall()
# connection.close()
# print(bool([]))

from filmorate.model.Genre import Genre
genres = [{"id": 1}, {"id": 2}, {"id": 1}]
a = list(set(map(lambda x: Genre(**x), genres)))
print(a)
