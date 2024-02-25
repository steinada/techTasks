from filmorate.model.Genre import Genre
from filmorate.model.Mpa import Mpa


class Film:
    def __init__(self, id=None, name=None, description=None, releaseDate=None, duration=None,
                 rate=None, mpa=None, genres=None):
        self.id = id
        self.name = name
        self.description = description
        self.release_date = releaseDate
        self.duration = duration
        self.rate = rate
        self.mpa = Mpa(**mpa)
        self.genres = list(set(map(lambda x: Genre(**x), genres)))
