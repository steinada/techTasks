from filmorate_mongo.app.repository import current_db


genre_collection = current_db["genre"]
id_collection = current_db["id_generator"]


class GenreRepository:
    @classmethod
    def get_all_genre_ids(cls):
        genre_ids = genre_collection.find(projection={'id': 1, '_id': 0})
        return genre_ids

    def get_genre_by_id(self, id):
        genres = genre_collection.find_one(filter={'id': id}, projection={'_id': 0})
        return genres

    def get_genres(self):
        genres = genre_collection.find(projection={'_id': 0})
        return genres

