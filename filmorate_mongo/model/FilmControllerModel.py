from filmorate.model.Genre import Genre
from filmorate.model.Mpa import Mpa
from filmorate.model.Director import Director


class FilmControllerModel:
    def __init__(self, id=None, name=None, description=None, release_date=None, duration=None,
                 rate=None, mpa=None, genres=None, director=None):
        self.id = id
        self.name = name
        self.description = description
        self.releaseDate = release_date
        self.duration = duration
        self.rate = rate
        self.mpa = vars(Mpa(id=mpa)) if mpa is not None and mpa is not None else None
        self.genres = list(map(lambda x: vars(Genre(id=x)), genres)) if genres is not None else []
        self.director = list(map(lambda x: vars(Director(id=x)), director)) if director is not None else []
