from filmorate.model.FilmControllerModel import FilmControllerModel
from datetime import datetime
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
db.execute(""" SELECT f.*, m.*, g.*, d.*, COUNT(DISTINCT(l.id)) AS likes
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
params_list = a
keys = ('id', 'name', 'description', 'release_date', 'duration', 'mpa_id', 'mpa_name', 'genre_id', 'genre_name',
        'director_id', 'director_name')
films_dict = [dict(zip(keys, film)) for film in params_list]
films_obj_dict = dict()
for film in films_dict:
    if film['id'] not in films_obj_dict:
        film_obj = FilmControllerModel(id=film['id'], name=film['name'], description=film['description'],
                        release_date=film['release_date'], duration=film['duration'])
        film_obj.release_date = str(datetime.fromisoformat(film_obj.releaseDate).date())
        film_obj.genres = [{'id': film['genre_id'], 'name': film['genre_name']}]
        film_obj.mpa = {'id': film['mpa_id'], 'name': film['mpa_name']}
        film_obj.director = [{'id': film['director_id'], 'name': film['director_name']}]
        films_obj_dict.update({film['id']: film_obj})
    else:
        films_obj_dict[film['id']].director.append({'id': film['director_id'], 'name': film['director_name']})
        films_obj_dict[film['id']].genres.append({'id': film['genre_id'], 'name': film['genre_name']})
films_json = list(map(lambda x: vars(x[1]), films_obj_dict.items()))
print(films_json)
# user_one, user_two = 2, 1
# user_one, user_two = sorted(user_one, user_two)
# print(user_one, user_two)
