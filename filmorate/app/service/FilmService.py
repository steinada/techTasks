from datetime import datetime, date
from filmorate.app.repository.FilmRepository import FilmRepository
from filmorate.app.service.Errors import InsertionError
import logging


class FilmService:

    @staticmethod
    def user_validator(func):
        def wrapper(obj):
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
            return func(obj)
        return wrapper

    @staticmethod
    def id_validator(func):
        def wrapper(obj):
            created_films = FilmRepository.get_created_films()
            created_films_list = list(map(lambda x: x[0], created_films))
            if obj.id not in created_films_list:
                logging.error(f"Film {obj.id} not found")
                raise InsertionError("film not created", 404)
            return func(obj)
        return wrapper

    @staticmethod
    @user_validator
    def add_film(film):
        release_date_date = datetime.fromisoformat(film.release_date)
        params = (film.name, film.description, release_date_date, film.duration)
        id = FilmRepository.add_film(params)
        if film.rate is not None:
            params = (id, film.rate)
            FilmRepository.set_rate(params)
        logging.info(f"Film created: id={id}, {str(vars(film))}")
        return id

    @staticmethod
    @id_validator
    @user_validator
    def update_film(film):
        release_date_date = datetime.fromisoformat(film.release_date)
        params = (film.name, film.description, release_date_date, film.duration, film.id)
        FilmRepository.update_film(params)
        logging.info(f"Film updated: {str(vars(film))}")

    @staticmethod
    def get_films():
        films = FilmRepository.get_films()
        keys = ('id', 'name', 'description', 'releaseDate', 'duration')
        films_list = [dict(zip(keys, film)) for film in films]
        for film in films_list:
            film['releaseDate'] = str(datetime.fromisoformat(film['releaseDate']).date())
        return films_list

