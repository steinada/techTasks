from flask import Blueprint
from filmorate.model.Mpa import Mpa
from filmorate.app.service.MpaService import MpaService


blueprint = Blueprint('mpa', __name__)
mpa_service = MpaService()


@blueprint.get('/<string:id>')
def get_genre(id):
    id = int(id)
    mpa_to_find = Mpa(id=id)
    mpa = mpa_service.get_mpa_by_id(mpa_to_find)
    return vars(mpa), 200


@blueprint.get('')
def get_all_mpa():
    mpas = mpa_service.get_all_mpa()
    mpas_json = [vars(mpa) for mpa in mpas]
    return mpas_json, 200

