from flask import request, Blueprint
from filmorate_mongo.model.Film import Film
from filmorate_mongo.model.User import User
from filmorate_mongo.app.service.FilmService import FilmService
from filmorate_mongo.model.FilmControllerModel import FilmControllerModel
from filmorate_mongo.app.service.GenreService import GenreService
from filmorate_mongo.app.service.MpaService import MpaService
from filmorate_mongo.app.service.DirectorService import DirectorService


blueprint = Blueprint('films', __name__)
film_service = FilmService()
genre_service = GenreService()
mpa_service = MpaService()
director_service = DirectorService()


@blueprint.post('')
def add_film():
    params = request.json
    film = Film(**params)
    film = film_service.add_film(film)
    film_controller = FilmControllerModel(**film)
    return vars(film_controller)


@blueprint.put('')
def update_film():
    params = request.json
    film = Film(**params)
    film_updated = film_service.update_film(film)
    film_controller = FilmControllerModel(**film_updated)
    return vars(film_controller)


@blueprint.get('')
def get_all_films():
    films = film_service.get_films()
    return films


@blueprint.put('/<string:id>/like/<string:user_id>')
def set_like_to_film(id, user_id):
    id, user_id = int(id), int(user_id)
    film = Film(id=id)
    user = User(id=user_id)
    film_service.set_like(film, user)
    return {"result": "ok"}, 200


@blueprint.delete('<string:id>/like/<string:user_id>')
def delete_like_from_film(id, user_id):
    id, user_id = int(id), int(user_id)
    film = Film(id=id)
    user = User(id=user_id)
    film_service.delete_like(film, user)
    return {"result": "ok"}, 200


@blueprint.get('/popular')
def get_most_popular_films():
    count = request.args.get('count')
    if count is None:
        count = 10
    else:
        count = int(count)
    popular_films = film_service.get_popular_films(count)
    return popular_films, 200


@blueprint.get('/<string:id>')
def get_film_by_id(id):
    id = int(id)
    film = Film(id=id)
    film = film_service.get_film_by_id(film)
    return film, 200


@blueprint.get('/search')
def get_films_by_params():
    query = request.args.get('query')
    sort_by = request.args.get('by').split(',') if request.args.get('by') is not None else []
    films = film_service.get_films_by_params(query, sort_by)
    return films
