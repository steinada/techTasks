from filmorate_mongo.app.repository.GenreRepository import GenreRepository
from filmorate_mongo.app.service.Errors import InsertionError
from filmorate_mongo.model.Genre import Genre
import logging


class GenreService:
    def __init__(self):
        self.genre_repository = GenreRepository()

    @staticmethod
    def genre_id_validator(func):
        def wrapper(self, objs):
            genre_objs = filter(lambda x: isinstance(x, Genre), objs)
            created_genres = GenreRepository.get_all_genre_ids()
            created_genres_list = list(map(lambda x: x['id'], created_genres))
            for obj in genre_objs:
                if obj.id < 0:
                    logging.error(f"Genre {obj.id} is incorrect")
                    raise InsertionError("Genre id is incorrect", 404)
                if obj.id not in created_genres_list:
                    logging.error(f"Genre {obj.id} not found")
                    raise InsertionError("Genre not created", 404)
            return func(self, *objs)

        return wrapper

    def get_genre_by_id(self, genre):
        id = genre.id
        genre = self.genre_repository.get_genre_by_id(id)
        if not genre:
            logging.error(f"genre with id {id} not found")
            raise InsertionError("genre not found", 404)
        return genre

    def get_genres(self):
        genres = self.genre_repository.get_genres()
        genres_list = list(map(lambda x: x, genres))
        return genres_list
