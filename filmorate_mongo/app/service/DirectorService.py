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
            created_directors = DirectorRepository.get_all_directors()
            created_directors_list = list(map(lambda x: x['id'], created_directors))
            for obj in director_objs:
                if obj.id not in created_directors_list:
                    logging.error(f"Director {obj.name} not found")
                    raise InsertionError("director not created", 404)
            return func(self, *objs)
        return wrapper

    def get_all_directors(self):
        directors = self.directors_repository.get_all_directors()
        directors_list = list(map(lambda x: x, directors))
        return directors_list

    def add_director(self, director):
        id = self.directors_repository.id_generator()
        director.id = id
        params = vars(director)
        object_id = self.directors_repository.add_director(params)
        logging.info(f"Director created: id={object_id}, {str(params)}")
        del params['_id']
        return params

    @id_validator
    def update_director(self, director):
        director = self.directors_repository.update_director(params=director.name, id=director.id)
        return director

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
