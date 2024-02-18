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


