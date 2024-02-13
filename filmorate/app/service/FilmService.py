from datetime import datetime
from filmorate.app.repository.FilmRepository import FilmRepository


class FilmService:
    @staticmethod
    def add_film(film):
        release_date_date = datetime.fromisoformat(film.release_date)
        params = (film.name, film.description, release_date_date, film.duration)
        id = FilmRepository.add_film(params)
        return id

    @staticmethod
    def update_film(film):
        release_date_date = datetime.fromisoformat(film.release_date)
        params = (film.name, film.description, release_date_date, film.duration, film.id)
        FilmRepository.update_film(params)

    @staticmethod
    def get_films():
        films = FilmRepository.get_films()
        keys = ('id', 'name', 'description', 'releaseDate', 'duration')
        films_list = [dict(zip(keys, film)) for film in films]
        for film in films_list:
            film['releaseDate'] = str(datetime.fromisoformat(film['releaseDate']).date())
        return films_list

