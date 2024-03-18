import sqlite3


db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"


class GenreRepository:
    @classmethod
    def get_all_genre_ids(cls, ids):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT id FROM genre WHERE id IN ({ids}) """.format(ids=ids))
        genres = db.fetchall()
        connection.close()
        return genres

    def get_genre_by_id(self, id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM genre WHERE id = {id} """.format(id=id))
        genre = db.fetchall()
        connection.close()
        return genre

    def get_genres(self):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM genre """)
        genres = db.fetchall()
        connection.close()
        return genres

    def set_film_genres(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO film_genre (genre_id, film_id)
                    VALUES {params}""".format(params=params))
        connection.commit()
        connection.close()

    def get_films_genres(self, ids):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT fg.film_id, fg.genre_id, g.name
                    FROM film_genre fg, genre g
                    WHERE fg.film_id IN ({ids}) AND g.id = fg.genre_id """.format(ids=ids))
        films_genres = db.fetchall()
        connection.close()
        return films_genres

    def delete_film_genres(self, film_id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" DELETE FROM film_genre
                    WHERE film_id = {film_id} """.format(film_id=film_id))
        connection.commit()
        connection.close()

