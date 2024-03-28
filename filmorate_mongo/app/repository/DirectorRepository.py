from filmorate_mongo.app.repository import current_db

import pymongo


director_collection = current_db["director"]
id_collection = current_db["id_generator"]


class DirectorRepository:
    def id_generator(self):
        id = id_collection.find_one_and_update(
            {"collection": "director"},
            {"$inc": {"id": 1}},
            projection={"id": 1, "_id": 0},
            return_document=pymongo.ReturnDocument.AFTER)
        return id['id']

    @classmethod
    def get_all_directors(cls):
        directors = director_collection.find()
        return directors

    def add_director(self, params):
        director = director_collection.insert_one(params)
        object_id = director.inserted_id
        return object_id

    def update_director(self, id, params):
        film_update = director_collection.find_one_and_update(filter={'id': id}, update={'$set': params},
                                                          projection={'_id': 0},
                                                              return_document=pymongo.ReturnDocument.AFTER)
        return film_update

    def get_director_by_id(self, id):
        director = director_collection.find_one(filter={'id': id}, projection={'_id': 0})
        return director

    def get_created_directors(self):
        director_ids = director_collection.find(projection={'id': 1, '_id': 0})
        return director_ids

    def delete_director(self, id):
        director_collection.delete_one(filter={'id': id})

    def delete_director_from_films(self, director_id):
        director_collection.update_one(update={'$unset': {"director": director_id}})

