import sqlite3


db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"


class FilmRepository:
    @staticmethod
    def add_film(params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO
                film (name, description, release_date, duration)
                VALUES (?, ?, ?, ?) """, params)
        id = db.lastrowid
        connection.commit()
        connection.close()
        return id

    @staticmethod
    def update_film(params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" UPDATE film
                SET name = ?, description = ?, release_date = ?, duration = ?
                WHERE id = ?""", params)
        connection.commit()
        connection.close()

    @staticmethod
    def get_films():
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM film """)
        films = db.fetchall()
        connection.close()
        return films

    @staticmethod
    def get_created_films():
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT id FROM film """)
        film_ids = db.fetchall()
        connection.close()
        return film_ids

    @staticmethod
    def set_rate(params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO
                rate (film_id, rate)
                VALUES (?, ?) """, params)
        connection.commit()
        connection.close()
