from filmorate_mongo.app.repository.GenreRepository import GenreRepository
from filmorate_mongo.app.service.Errors import InsertionError
from filmorate_mongo.model.Genre import Genre
import logging


class GenreService:
    def __init__(self):
        self.genre_repository = GenreRepository()

    @staticmethod
    def genre_id_validator(func):
        def wrapper(self, film):
            genres_film = film.genres
            ids = list(map(lambda x: x.id, genres_film))
            ids_string = str(ids).strip("[]")
            genres = GenreRepository.get_all_genre_ids(ids_string)
            genre_ids = [id[0] for id in genres]
            not_created = set(ids) - set(genre_ids)
            if not_created:
                raise InsertionError(f"genre with id {', '.join(list(not_created))} is not created ")
            return func(self, film)
        return wrapper

    @genre_id_validator
    def set_genre_to_film(self, film):
        genres, film_id = film.genres, film.id
        self.genre_repository.delete_film_genres(film_id)
        if genres:
            genres_list = list(map(lambda x: x.id, genres))
            params_to_set = [(genre_id, film_id) for genre_id in genres_list]
            params_string = str(params_to_set).strip("[]")
            self.genre_repository.set_film_genres(params_string)

    def get_genre_by_id(self, genre):
        id = genre.id
        genre = self.genre_repository.get_genre_by_id(id)
        if not genre:
            logging.error(f"genre with id {id} not found")
            raise InsertionError("genre not found", 404)
        genre_values = genre[0]
        genre = Genre(id=genre_values[0], name=genre_values[1])
        return genre

    def get_genres(self):
        genres_list = self.genre_repository.get_genres()
        genres = [Genre(id=value[0], name=value[1]) for value in genres_list]
        return genres

    def get_genres_of_films(self, films_ids):
        ids_string = str(films_ids).strip("[]")
        genres_list = self.genre_repository.get_films_genres(ids_string)
        genres_dict = dict()
        for relation in genres_list:
            film_id, genre_id, genre_name = relation
            genres_dict[film_id] = genres_dict.get(film_id, list())
            genres_dict[film_id].append({"id": genre_id, "name": genre_name})
        return genres_dict
