from datetime import datetime
from filmorate.app.repository.FilmRepository import FilmRepository
from filmorate.app.service.Errors import InsertionError
from filmorate.app.service.UserService import UserService
from filmorate.app.service.GenreService import GenreService
from filmorate.app.service.MpaService import MpaService
from filmorate.model.Film import Film
from filmorate.model.FilmControllerModel import FilmControllerModel
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
            created_films_list = list(map(lambda x: x[0], created_films))
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
        keys = ('id', 'name', 'description', 'release_date', 'duration', 'mpa_id', 'mpa_name', 'genre_id', 'genre_name',
                'director_id', 'director_name')
        films_dict = [dict(zip(keys, film)) for film in params_list]
        films_obj_dict = dict()
        for film in films_dict:
            if film['id'] not in films_obj_dict:
                film_obj = FilmControllerModel(id=film['id'], name=film['name'], description=film['description'],
                release_date=film['release_date'], duration=film['duration'])
                film_obj.releaseDate = str(datetime.fromisoformat(film_obj.releaseDate).date())
                film_obj.genres = [{'id': film['genre_id'], 'name': film['genre_name']}]\
                    if film['genre_id'] is not None else []
                film_obj.mpa = {'id': film['mpa_id'], 'name': film['mpa_name']}\
                    if film['mpa_id'] is not None else None
                film_obj.director = [{'id': film['director_id'], 'name': film['director_name']}]\
                    if film['director_id'] is not None else []
                films_obj_dict.update({film['id']: film_obj})
            else:
                if film['director_id']:
                    films_obj_dict[film['id']].director.append({'id': film['director_id'], 'name': film['director_name']})
                if film['genre_id']:
                    films_obj_dict[film['id']].genres.append({'id': film['genre_id'], 'name': film['genre_name']})
        films_json = list(map(lambda x: vars(x[1]), films_obj_dict.items()))
        return films_json

    @user_validator
    def add_film(self, film):
        release_date_date = datetime.fromisoformat(film.release_date)
        params = (film.name, film.description, release_date_date, film.duration)
        id = self.film_repository.add_film(params)
        if film.rate is not None:
            params = (id, film.rate)
            self.film_repository.set_rate(params)
        logging.info(f"Film created: id={id}, {str(vars(film))}")
        return id

    @id_validator
    @user_validator
    def update_film(self, film):
        release_date_date = datetime.fromisoformat(film.release_date)
        params = (film.name, film.description, release_date_date, film.duration, film.id)
        self.film_repository.update_film(params)
        logging.info(f"Film updated: {str(vars(film))}")

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
        popular_films_list = FilmService.make_film_json(popular_films)
        return popular_films_list

    @id_validator
    def get_film_by_id(self, film):
        film = self.film_repository.get_film_by_id(film.id)
        film = FilmService.make_film_json(film)
        return film[0]

    def get_films_by_params(self, query, sort_by):
        films = self.film_repository.get_films_by_params(query, sort_by)
        films_json = self.make_film_json(films)
        return films_json


