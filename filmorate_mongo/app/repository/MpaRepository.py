from filmorate_mongo.app.repository import current_db


mpa_collection = current_db["mpa"]
id_collection = current_db["id_generator"]


class MpaRepository:
    def get_mpas(self):
        mpas = mpa_collection.find(projection={'_id': 0})
        return mpas

    def get_mpa_by_id(self, id):
        mpa = mpa_collection.find_one(filter={'id': id}, projection={'_id': 0})
        return mpa
