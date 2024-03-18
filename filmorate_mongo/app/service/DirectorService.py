from filmorate_mongo.app.repository.DirectorRepository import DirectorRepository
from filmorate_mongo.model.Director import Director
from filmorate_mongo.app.view.ErrorHandlers import InsertionError
from filmorate_mongo.app.service.FilmService import FilmService
import logging


class DirectorService:
    def __init__(self):
        self.directors_repository = DirectorRepository()
        self.film_service = FilmService()

    @staticmethod
    def id_validator(func):
        def wrapper(self, *objs):
            director_objs = filter(lambda x: isinstance(x, Director), objs)
            created_directors = DirectorRepository.get_all_directors_id()
            created_directors_list = list(map(lambda x: x[0], created_directors))
            for obj in director_objs:
                if obj.id < 0:
                    logging.error(f"Film {obj.id} is incorrect")
                    raise InsertionError("director id is incorrect", 404)
                if obj.id not in created_directors_list:
                    logging.error(f"Film {obj.id} not found")
                    raise InsertionError("director not created", 404)
            return func(self, *objs)
        return wrapper

    def get_all_directors(self):
        directors_list = self.directors_repository.get_directors()
        directors = [Director(id=value[0], name=value[1]) for value in directors_list]
        return directors

    def add_director(self, director):
        id = self.directors_repository.add_director(director.name)
        return id

    @id_validator
    def update_director(self, director):
        params = (director.name, director.id)
        self.directors_repository.update_director(params)

    @id_validator
    def get_director_by_id(self, director):
        director = self.directors_repository.get_director_by_id(director.id)[0]
        keys = ("id", "name")
        director_obj = Director(**dict(zip(keys, director)))
        return director_obj

    @id_validator
    def delete_director(self, director):
        self.directors_repository.delete_director_from_films(director.id)
        self.directors_repository.delete_director(director.id)

    @id_validator
    def set_film_director(self, film):
        directors, film_id = film.director, film.id
        self.directors_repository.delete_film_director(film_id)
        if directors:
            directors_list = list(map(lambda x: x.id, directors))
            params_to_set = [(director_id, film_id) for director_id in directors_list]
            params_string = str(params_to_set).strip("[]")
            self.directors_repository.set_film_director(params_string)

