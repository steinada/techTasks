import sqlite3


db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"


class FilmRepository:
    def add_film(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO
                film (name, description, release_date, duration)
                VALUES (?, ?, ?, ?) """, params)
        id = db.lastrowid
        connection.commit()
        connection.close()
        return id

    def update_film(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" UPDATE film
                SET name = ?, description = ?, release_date = ?, duration = ?
                WHERE id = ?""", params)
        connection.commit()
        connection.close()

    def get_films(self):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM film """)
        films = db.fetchall()
        connection.close()
        return films

    def get_created_films(self):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT id FROM film """)
        film_ids = db.fetchall()
        connection.close()
        return film_ids

    def set_rate(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO
                rate (film_id, rate)
                VALUES (?, ?) """, params)
        connection.commit()
        connection.close()

    def set_like(self, film_id, user_id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO
                        like (user_id, film_id)
                        VALUES (?, ?) """, (user_id, film_id))
        connection.commit()
        connection.close()

    def delete_like(self, film_id, user_id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" DELETE FROM like 
                        WHERE user_id = ? AND film_id = ? """, (user_id, film_id))
        connection.commit()
        connection.close()

    def get_popular_films(self, count):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM film f
                        LEFT JOIN like l ON f.id = l.film_id
                        GROUP BY f.id
                        ORDER BY COUNT(l.user_id) DESC
                        LIMIT {count} """.format(count=count))
        popular_films = db.fetchall()
        connection.close()
        return popular_films

    def get_film_by_id(self, id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM film WHERE id = {id} """.format(id=id))
        film = db.fetchall()
        connection.close()
        return film

    def get_films_by_params(self, query, sort_by):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        sorting, where, sort_dict = '', '', {'director': 'd.name', 'title': 'f.name'}
        for param in sort_by:
            sorting += f", {sort_dict[param]}"
        if query:
            where += f"WHERE f.name LIKE '%{query}%'"
        db.execute(""" SELECT f.*, COUNT(DISTINCT(l.id)) AS likes
                            FROM film f
                            LEFT JOIN film_director fd ON fd.film_id = f.id
                            LEFT JOIN director d ON d.id = fd.director_id
                            LEFT JOIN film_genre fg ON fg.film_id = f.id
                            LEFT JOIN genre g ON g.id = fg.genre_id
                            LEFT JOIN film_mpa fm ON fm.film_id = f.id
                            LEFT JOIN mpa m ON m.id = fm.mpa_id
                            LEFT JOIN like l ON l.film_id = f.id
                            {where}
                            GROUP BY f.id, fd.id, fg.id
                            ORDER BY likes DESC {sorting} """.format(sorting=sorting, where=where))
        films = db.fetchall()
        connection.close()
        return films
