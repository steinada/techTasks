import sqlite3


db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"


class DirectorRepository:
    @classmethod
    def get_all_directors_id(cls):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT id FROM director """)
        directors_id = db.fetchall()
        connection.close()
        return directors_id

    def get_directors(self):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM director """)
        directors = db.fetchall()
        connection.close()
        return directors

    def add_director(self, name):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO director (name)
                    VALUES (?) """, (name,))
        id = db.lastrowid
        connection.commit()
        connection.close()
        return id

    def update_director(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" UPDATE director
                SET name = ?
                WHERE id = ?""", params)
        connection.commit()
        connection.close()

    def get_director_by_id(self, id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM director WHERE id = {id} """.format(id=id))
        director = db.fetchall()
        connection.close()
        return director

    def delete_director(self, id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" DELETE FROM director WHERE id = {id} """.format(id=id))
        connection.commit()
        connection.close()

    def delete_director_from_films(self, director_id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" DELETE FROM film_director WHERE director_id = {director_id} """.format(director_id=director_id))
        connection.commit()
        connection.close()

    def delete_film_director(self, film_id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" DELETE FROM film_director WHERE film_id = {film_id} """.format(film_id=film_id))
        connection.commit()
        connection.close()

    def set_film_director(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO film_director (director_id, film_id)
                    VALUES {params}""".format(params=params))
        connection.commit()
        connection.close()

