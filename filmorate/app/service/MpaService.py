from filmorate.app.repository.MpaRepository import MpaRepository
from filmorate.app.service.Errors import InsertionError
from filmorate.model.Mpa import Mpa
import logging


class MpaService:
    def __init__(self):
        self.mpa_repository = MpaRepository()

    def get_all_mpa(self):
        mpa_list = self.mpa_repository.get_mpas()
        mpas = [Mpa(id=value[0], name=value[1]) for value in mpa_list]
        return mpas

    def get_mpa_by_id(self, mpa):
        id = mpa.id
        mpa = self.mpa_repository.get_mpa_by_id(id)
        if not mpa:
            logging.error(f"mpa with id {id} not found")
            raise InsertionError("mpa not found", 404)
        mpa_values = mpa[0]
        mpa = Mpa(id=mpa_values[0], name=mpa_values[1])
        return mpa

    def set_mpa_to_film(self, film):
        mpa_id, film_id = film.mpa.id, film.id
        params_to_set = (mpa_id, film_id)
        self.mpa_repository.set_film_mpa(params_to_set)

    def get_mpa_of_films(self, films_ids):
        ids_string = str(films_ids).strip("[]")
        mpa_list = self.mpa_repository.get_films_mpa(ids_string)
        mpa_dict = {film_id: {"id": mpa_id, "name": mpa_name} for film_id, mpa_id, mpa_name in mpa_list}
        return mpa_dict

