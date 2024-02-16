class FilmControllerModel:
    def __init__(self, id=None, name=None, description=None, release_date=None, duration=None, rate=None):
        self.id = id
        self.name = name
        self.description = description
        self.releaseDate = release_date
        self.duration = duration
        self.rate = rate