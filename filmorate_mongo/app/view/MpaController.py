from flask import Blueprint
from filmorate_mongo.model.Mpa import Mpa
from filmorate_mongo.app.service.MpaService import MpaService


blueprint = Blueprint('mpa', __name__)
mpa_service = MpaService()


@blueprint.get('/<string:id>')
def get_mpa(id):
    id = int(id)
    mpa_to_find = Mpa(id=id)
    mpa = mpa_service.get_mpa_by_id(mpa_to_find)
    return mpa, 200


@blueprint.get('')
def get_all_mpa():
    mpas = mpa_service.get_all_mpa()
    return mpas, 200

