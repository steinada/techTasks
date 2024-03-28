from datetime import datetime
from filmorate_mongo.app.repository.FilmRepository import FilmRepository
from filmorate_mongo.app.service.Errors import InsertionError
from filmorate_mongo.app.service.UserService import UserService
from filmorate_mongo.app.service.GenreService import GenreService
from filmorate_mongo.app.service.MpaService import MpaService
from filmorate_mongo.model.Film import Film
from filmorate_mongo.model.FilmControllerModel import FilmControllerModel
from filmorate_mongo.model.FilmDTO import FilmDTO
import logging


class FilmService:
    def __init__(self):
        self.film_repository = FilmRepository()
        self.genre_service = GenreService()
        self.mpa_service = MpaService()

    @staticmethod
    def user_validator(func):
        def wrapper(self, obj):
            if len(obj.description) > 200:
                logging.error(f"Description {obj.description} is longer then 200 chars")
                raise InsertionError("description error", 400)
            if int(obj.duration) <= 0:
                logging.error(f"Duration {obj.duration} is or less then 0")
                raise InsertionError("duration error", 400)
            if obj.name == "" or obj.name is None:
                logging.error(f"Name {obj.name} is not a word")
                raise InsertionError("name error", 400)
            if datetime.fromisoformat(obj.release_date) < datetime.fromisoformat('1895-12-28'):
                logging.error(f"Release date {obj.release_date} is future date")
                raise InsertionError("release date error", 400)
            return func(self, obj)
        return wrapper

    @staticmethod
    def id_validator(func):
        def wrapper(self, *objs):
            film_objs = filter(lambda x: isinstance(x, Film), objs)
            created_films = self.film_repository.get_created_films()
            created_films_list = list(map(lambda x: x['id'], created_films))
            for obj in film_objs:
                if obj.id < 0:
                    logging.error(f"Film {obj.id} is incorrect")
                    raise InsertionError("film id is incorrect", 404)
                if obj.id not in created_films_list:
                    logging.error(f"Film {obj.id} not found")
                    raise InsertionError("film not created", 404)
            return func(self, *objs)
        return wrapper

    @staticmethod
    def make_film_json(params_list):
        films_obj_dict = dict()
        for film in params_list:
            if film['id'] not in films_obj_dict:
                film_obj = FilmControllerModel(id=film['id'], name=film['name'], description=film['description'],
                release_date=film['release_date'], duration=film['duration'], rate=film['rate'])
                film_obj.genres = [{'id': film['genre_info'][0]['id'], 'name': film['genre_info'][0]['name']}]\
                    if film['genre_info'] else []
                film_obj.mpa = {'id': film['mpa_info'][0]['id'], 'name': film['mpa_info'][0]['name']}\
                    if film['mpa_info'] is not None else None
                film_obj.director = [{'id': film['director_info'][0]['id'], 'name': film['director_info'][0]['name']}]\
                    if film['director_info'] else []
                films_obj_dict.update({film['id']: film_obj})
            else:
                if (film['director_info']
                        and {'id': film['director_info'][0]['id'],
                             'name': film['director_info'][0]['name']}
                        not in films_obj_dict[film['id']].director):
                    (films_obj_dict[film['id']].director
                     .append({'id': film['director_info'][0]['id'], 'name': film['director_info'][0]['name']}))
                if (film['genre_info']
                        and {'id': film['genre_info'][0]['id'],
                             'name': film['genre_info'][0]['name']}
                        not in films_obj_dict[film['id']].genres):
                    (films_obj_dict[film['id']].genres
                     .append({'id': film['genre_info'][0]['id'], 'name': film['genre_info'][0]['name']}))
        films_json = list(map(lambda x: vars(x[1]), films_obj_dict.items()))
        return films_json

    @user_validator
    def add_film(self, film):
        film.id = self.film_repository.id_generator()
        film_dto = FilmDTO(**vars(film))
        params = vars(film_dto)
        object_id = str(self.film_repository.add_film(params))
        logging.info(f"Film created: id={object_id}, {str(params)}")
        del params['_id']
        del params['likes_count']
        return params

    @id_validator
    @user_validator
    def update_film(self, film):
        film_dto = FilmDTO(**vars(film))
        params = vars(film_dto)
        film_updated = self.film_repository.update_film(params, film.id)
        logging.info(f"Film updated: {str(film_updated)}")
        del film_updated['_id']
        del params['likes_count']
        return film_updated

    def get_films(self):
        films = self.film_repository.get_films()
        films_list = FilmService.make_film_json(films)
        return films_list

    @UserService.id_validator
    @id_validator
    def set_like(self, film, user):
        self.film_repository.set_like(film.id, user.id)

    @UserService.id_validator
    @id_validator
    def delete_like(self, film, user):
        self.film_repository.delete_like(film.id, user.id)

    def get_popular_films(self, count):
        popular_films = self.film_repository.get_popular_films(count)
        film_objs = [row['allFields'] for row in popular_films]
        film_rows = list()
        for film_row in film_objs:
            film_rows.extend(film_row)
        popular_films_list = FilmService.make_film_json(film_rows)
        return popular_films_list

    @id_validator
    def get_film_by_id(self, film):
        film = self.film_repository.get_film_by_id(film.id)
        film = FilmService.make_film_json(film)
        return film[0]

    def get_films_by_params(self, query, sort_by):
        films = self.film_repository.get_films_by_params(query, sort_by)
        film_objs = [row['allFields'] for row in films]
        film_rows = list()
        for film_row in film_objs:
            film_rows.extend(film_row)
        popular_films_list = FilmService.make_film_json(film_rows)
        return popular_films_list


