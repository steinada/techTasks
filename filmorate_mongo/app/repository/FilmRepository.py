from filmorate_mongo.app.repository import current_db

import pymongo
import re


film_collection = current_db["film"]
id_collection = current_db["id_generator"]


class FilmRepository:
    def id_generator(self):
        id = id_collection.find_one_and_update(
            {"collection": "film"},
            {"$inc": {"id": 1}},
            projection={"id": 1, "_id": 0},
            return_document=pymongo.ReturnDocument.AFTER)
        return id['id']

    def add_film(self, params):
        film = film_collection.insert_one(params)
        object_id = film.inserted_id
        return object_id

    def update_film(self, params, id):
        film_update = film_collection.find_one_and_update(filter={'id': id}, update={'$set': params},
            return_document=pymongo.ReturnDocument.AFTER, projection={'likes_count': 0, 'likes': 0})
        return film_update

    def get_films(self):
        pipeline = [
            {
                "$unwind": {"path": "$genres",
                            "preserveNullAndEmptyArrays": True}
            },
            {
                "$unwind": {"path": "$director",
                            "preserveNullAndEmptyArrays": True}
            },
            {
                "$lookup": {
                    "from": "genre",
                    "localField": "genres",
                    "foreignField": "id",
                    "as": "genre_info"
                }
            },
            {
                "$lookup": {
                    "from": "director",
                    "localField": "director",
                    "foreignField": "id",
                    "as": "director_info"
                }
            },
            {
                "$lookup": {
                    "from": "mpa",
                    "localField": "mpa",
                    "foreignField": "id",
                    "as": "mpa_info"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "mpa": 0,
                    "genres": 0,
                    "director": 0,
                    "genre_info._id": 0,
                    "mpa_info._id": 0,
                    "director_info._id": 0,
                    "likes_count": 0

                }
            }
        ]
        films = film_collection.aggregate(pipeline)
        return films

    def get_created_films(self):
        film_ids = film_collection.find(projection={'id': 1, '_id': 0})
        return film_ids

    def set_like(self, film_id, user_id):
        film_collection.update_one(filter={'id': film_id}, update={'$push': {"likes": user_id},
                                                                   '$inc': {'likes_count': 1}})

    def delete_like(self, film_id, user_id):
        film_collection.update_one(filter={'id': film_id}, update={'$unset': {"likes": user_id},
                                                                   '$dec': {'likes_count': 1}})

    def get_popular_films(self, count):
        pipeline = [
            {
                "$unwind": {"path": "$genres",
                            "preserveNullAndEmptyArrays": True}
            },
            {
                "$unwind": {"path": "$director",
                            "preserveNullAndEmptyArrays": True}
            },
            {
                "$lookup": {
                    "from": "genre",
                    "localField": "genres",
                    "foreignField": "id",
                    "as": "genre_info"
                }
            },
            {
                "$lookup": {
                    "from": "director",
                    "localField": "director",
                    "foreignField": "id",
                    "as": "director_info"
                }
            },
            {
                "$lookup": {
                    "from": "mpa",
                    "localField": "mpa",
                    "foreignField": "id",
                    "as": "mpa_info"
                }
            },
            {
                '$group': {
                    "_id": "$_id",
                    'allFields': {'$push': "$$ROOT"}
                }
            },
            {
                '$sort': {
                    'allFields.likes_count': -1
                }
            },
            {
                '$limit': count
            },
            {
                "$project": {
                    "_id": 0,
                    "mpa": 0,
                    "genres": 0,
                    "director": 0
                }
            }
        ]
        films = film_collection.aggregate(pipeline)
        return films

    def get_film_by_id(self, id):
        pipeline = [
            {
                "$unwind": {"path": "$genres",
                            "preserveNullAndEmptyArrays": True}
            },
            {
                "$unwind": {"path": "$director",
                            "preserveNullAndEmptyArrays": True}
            },
            {
                "$match": {
                    "id": id
                }
            },
            {
                "$lookup": {
                    "from": "genre",
                    "localField": "genres",
                    "foreignField": "id",
                    "as": "genre_info"
                }
            },
            {
                "$lookup": {
                    "from": "director",
                    "localField": "director",
                    "foreignField": "id",
                    "as": "director_info"
                }
            },
            {
                "$lookup": {
                    "from": "mpa",
                    "localField": "mpa",
                    "foreignField": "id",
                    "as": "mpa_info"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "mpa": 0,
                    "genres": 0,
                    "director": 0,
                    "genre_info._id": 0,
                    "mpa_info._id": 0,
                    "director_info._id": 0,
                    "likes_count": 0
                }
            }
        ]
        film = film_collection.aggregate(pipeline)
        return film

    def get_films_by_params(self, query, sort_by):
        sorting = {'allFields.likes_count': -1}
        sort_dict = {'director': {'allFields.director_info.name': -1}, 'title': {'allFields.name': 1}}
        for param in sort_by:
            sorting.update(sort_dict[param])
        title_query = {'$match': {'allFields.name': {'$regex': re.compile(fr"{query}")}}}
        pipeline = [
            {
                "$unwind": {"path": "$genres",
                            "preserveNullAndEmptyArrays": True}
            },
            {
                "$unwind": {"path": "$director",
                            "preserveNullAndEmptyArrays": True}
            },
            {
                "$lookup": {
                    "from": "genre",
                    "localField": "genres",
                    "foreignField": "id",
                    "as": "genre_info"
                }
            },
            {
                "$lookup": {
                    "from": "director",
                    "localField": "director",
                    "foreignField": "id",
                    "as": "director_info"
                }
            },
            {
                "$lookup": {
                    "from": "mpa",
                    "localField": "mpa",
                    "foreignField": "id",
                    "as": "mpa_info"
                }
            },
            {
                '$group': {
                    "_id": "$_id",
                    'allFields': {'$push': "$$ROOT"}
                }
            },
            {
                '$sort': sorting
            },
            title_query,

            {
                "$project": {
                    "_id": 0,
                    "mpa": 0,
                    "genres": 0,
                    "director": 0,
                    "genre_info._id": 0,
                    "mpa_info._id": 0,
                    "director_info._id": 0,
                    "likes_count": 0
                }
            }
        ]
        films = film_collection.aggregate(pipeline)
        return films
