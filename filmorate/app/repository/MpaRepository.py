import sqlite3


db_path = "C:\\Users\\stein\\PycharmProjects\\techTasks\\filmorate\\filmorate.db"


class MpaRepository:
    @classmethod
    def get_all_mpa_ids(cls, ids):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT id FROM mpa WHERE id IN ({ids}) """.format(ids=ids))
        mpa = db.fetchall()
        connection.close()
        return mpa

    def get_mpas(self):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM mpa """)
        mpa = db.fetchall()
        connection.close()
        return mpa

    def get_mpa_by_id(self, id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT * FROM mpa WHERE id = {id} """.format(id=id))
        mpa = db.fetchall()
        connection.close()
        return mpa

    def set_film_mpa(self, params):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" INSERT INTO film_mpa (mpa_id, film_id)
                    VALUES {params}""".format(params=params))
        connection.commit()
        connection.close()

    def get_films_mpa(self, ids):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" SELECT fm.film_id, fm.mpa_id, m.name
                    FROM film_mpa fm, mpa m
                    WHERE fm.film_id IN ({ids}) AND m.id = fm.mpa_id """.format(ids=ids))
        films_mpa = db.fetchall()
        connection.close()
        return films_mpa

    def delete_film_mpas(self, film_id):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        db = connection.cursor()
        db.execute(""" DELETE FROM film_mpa WHERE film_id = ? """, (film_id, ))
        connection.commit()
        connection.close()

