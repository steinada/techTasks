class FilmDTO:
    def __init__(self, id=None, name=None, description=None, release_date=None, duration=None,
                 rate=None, mpa=None, genres=None, director=None):
        self.id = id
        self.name = name
        self.description = description
        self.release_date = release_date
        self.duration = duration
        self.rate = rate
        self.mpa = mpa.id if mpa is not None else None
        self.genres = sorted(list(set(map(lambda x: x.id, genres)))) if genres is not None else None
        self.director = list(set(map(lambda x: x.id, director))) if director is not None else None
        self.likes_count = 0
