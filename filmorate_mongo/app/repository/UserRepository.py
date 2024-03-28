from filmorate_mongo.app.repository import current_db

import pymongo


user_collection = current_db["user"]
id_collection = current_db["id_generator"]


class UserRepository:
    def id_generator(self):
        id = id_collection.find_one_and_update(
            {"collection": "user"},
            {"$inc": {"id": 1}},
            projection={"id": 1, "_id": 0},
            return_document=pymongo.ReturnDocument.AFTER)
        return id['id']

    def add_user(self, params):
        user = user_collection.insert_one(params)
        object_id = user.inserted_id
        return object_id

    def update_user(self, params, id):
        user_update = user_collection.update_one(filter={'id': id}, update={'$set': params})
        return user_update

    def get_users(self):
        users = user_collection.find(projection={'_id': 0, 'friends': 0})
        return users

    @classmethod
    def get_created_users(cls):
        user_ids = user_collection.find(projection={'id': 1, '_id': 0})
        return user_ids

    def add_friend(self, user_one, user_two):
        user_collection.update_one(filter={'id': user_one}, update={'$push': {"friends": user_two}})

    def delete_friend(self, user_one, user_two):
        user_collection.update_one(filter={'id': user_one}, update={'$pull': {"friends": user_two}})

    def get_friends_of_user(self, user_id):
        pipeline = [
            {
                "$unwind": "$friends"
            },
            {
                "$match": {
                    "id": user_id
                }
            },
            {
                "$lookup": {
                    "from": "user",
                    "localField": "friends",
                    "foreignField": "id",
                    "as": "friends_info"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "friends_info.id": 1,
                    "friends_info.name": 1,
                    "friends_info.email": 1,
                    "friends_info.login": 1,
                    "friends_info.birthday": 1
                }
            }
        ]
        result = user_collection.aggregate(pipeline)
        return result

    def get_user_by_id(self, id):
        user = user_collection.find_one({'id': id}, projection={'_id': 0, 'friends': 0})
        return user

    def get_common_friends(self, user_one, user_two):
        pipeline = [
            {
                "$unwind": "$friends"
            },
            {
                "$match": {"id":
                               {"$in": [user_one, user_two]}
                           }
            },
            {
                "$lookup": {
                    "from": "user",
                    "localField": "friends",
                    "foreignField": "id",
                    "as": "friends_info"
                }
            },
            {
                "$lookup": {
                    "from": "friends_info",
                    "localField": "id",
                    "foreignField": "id",
                    "as": "friends_info2"
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "friends_info.id": 1,
                    "friends_info.name": 1,
                    "friends_info.email": 1,
                    "friends_info.login": 1,
                    "friends_info.birthday": 1,
                    "friends_info2.id": 1
                }
            }
        ]
        result = user_collection.aggregate(pipeline)
        return result
