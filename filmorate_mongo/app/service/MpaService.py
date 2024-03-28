from filmorate_mongo.app.repository.MpaRepository import MpaRepository
from filmorate_mongo.app.service.Errors import InsertionError

import logging


class MpaService:
    def __init__(self):
        self.mpa_repository = MpaRepository()

    def get_all_mpa(self):
        mpas = self.mpa_repository.get_mpas()
        mpa_list = list(map(lambda x: x, mpas))
        return mpa_list

    def get_mpa_by_id(self, mpa):
        id = mpa.id
        mpa = self.mpa_repository.get_mpa_by_id(id)
        if not mpa:
            logging.error(f"mpa with id {id} not found")
            raise InsertionError("mpa not found", 404)
        return mpa
