from flask import request, Blueprint
from filmorate.app.service.DirectorService import DirectorService
from filmorate.model.Director import Director


blueprint = Blueprint('directors', __name__)
director_service = DirectorService()


@blueprint.get('')
def get_all_directors():
    directors = director_service.get_all_directors()
    directors_json = [vars(director) for director in directors]
    return directors_json, 200


@blueprint.post('')
def add_director():
    params = request.json
    director = Director(**params)
    id = director_service.add_director(director)
    director.id = id
    return vars(director)


@blueprint.put('')
def update_director():
    params = request.json
    director = Director(**params)
    director_service.update_director(director)
    return vars(director)


@blueprint.get('/<string:id>')
def get_director_by_id(id):
    id = int(id)
    director = Director(id=id)
    director = director_service.get_director_by_id(director)
    return vars(director), 200


@blueprint.delete('/<string:id>')
def delete_director(id):
    id = int(id)
    director = Director(id=id)
    director_service.delete_director(director)
    return {"result": "director deleted"}, 200
