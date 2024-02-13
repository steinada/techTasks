from flask import request, Blueprint
from filmorate.model.Film import Film
# from flask_classy import route
from filmorate.app.service.FilmService import FilmService


blueprint = Blueprint('films', __name__)
film_service = FilmService()

# class FilmController(FlaskView):
# film_service = FilmService()


@blueprint.route('', methods=['POST'])
def add_film():
    params = request.json
    film = Film(**params)
    id = film_service.add_film(film)
    film.id = id
    return vars(film)


@blueprint.route('', methods=['PUT'])
def update_film():
    params = request.json
    film = Film(**params)
    film_service.update_film(film)
    return vars(film)


@blueprint.route('', methods=['GET'])
def get_all_films():
    films = film_service.get_films()
    return films

