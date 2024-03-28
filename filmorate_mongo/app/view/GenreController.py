from flask import Blueprint
from filmorate_mongo.model.Genre import Genre
from filmorate_mongo.app.service.GenreService import GenreService


blueprint = Blueprint('genres', __name__)
genre_service = GenreService()


@blueprint.get('/<string:id>')
def get_genre(id):
    id = int(id)
    genre_to_find = Genre(id=id)
    genre = genre_service.get_genre_by_id(genre_to_find)
    return genre, 200


@blueprint.get('')
def get_genres():
    genres = genre_service.get_genres()
    return genres
