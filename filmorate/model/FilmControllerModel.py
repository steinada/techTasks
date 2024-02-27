class FilmControllerModel:
    def __init__(self, id=None, name=None, description=None, release_date=None, duration=None,
                 rate=None, mpa=None, genres=None):
        self.id = id
        self.name = name
        self.description = description
        self.releaseDate = release_date
        self.duration = duration
        self.rate = rate
        self.mpa = vars(mpa) if mpa is not None else None
        self.genres = list(map(lambda x: vars(x), genres)) if genres is not None else []
