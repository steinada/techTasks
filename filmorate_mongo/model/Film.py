from filmorate.model.Genre import Genre
from filmorate.model.Mpa import Mpa
from filmorate.model.Director import Director


class Film:
    def __init__(self, id=None, name=None, description=None, releaseDate=None, duration=None,
                 rate=None, mpa=None, genres=None, director=None):
        self.id = id
        self.name = name
        self.description = description
        self.release_date = releaseDate
        self.duration = duration
        self.rate = rate
        self.mpa = Mpa(**mpa) if mpa is not None else None
        self.genres = sorted(list(set(map(lambda x: Genre(**x), genres))), key=lambda y: y.id)\
            if genres is not None else None
        self.director = list(set(map(lambda x: Director(**x), director))) if director is not None else None
