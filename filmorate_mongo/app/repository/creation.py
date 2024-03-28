from filmorate_mongo.app.repository import current_db


# объявляем коллекции

genre_collection = current_db["genre"]
mpa_collection = current_db["mpa"]
user_collection = current_db["user"]
film_collection = current_db["film"]
friend_collection = current_db["friend"]
like_collection = current_db["like"]
rate_collection = current_db["rate"]
director_collection = current_db["director"]
id_collection = current_db["id_generator"]


#удаляем информацию коллекций, если та была ранее

genre_collection.drop()
mpa_collection.drop()
user_collection.drop()
film_collection.drop()
friend_collection.drop()
like_collection.drop()
rate_collection.drop()
director_collection.drop()
id_collection.drop()


#выставляем базовые значения, которые будут заполнять соответствующие поля в другой коллекции

genre = [{'id': 1, 'name': 'Комедия'}, {'id': 2, 'name': 'Драма'}, {'id': 3, 'name': 'Мультфильм'},
         {'id': 4, 'name': 'Триллер'}, {'id': 5, 'name': 'Документальный'}, {'id': 6, 'name': 'Боевик'}]
genre_collection.insert_many(genre)

mpa = [{'id': 1, 'name': 'G'}, {'id': 2, 'name': 'PG'}, {'id': 3, 'name': 'PG-13'}, {'id': 4, 'name': 'R'},
       {'id': 5, 'name': 'NC-17'}]
mpa_collection.insert_many(mpa)


#добавление генераторов id

id_collection.insert_one({
    'collection': 'user',
    'id': 0
})

id_collection.insert_one({
    'collection': 'director',
    'id': 0
})

id_collection.insert_one({
    'collection': 'film',
    'id': 0
})
