from flask import request, Blueprint
from filmorate_mongo.app.service.UserService import UserService
from filmorate_mongo.model.User import User


blueprint = Blueprint('users', __name__)
user_service = UserService()


@blueprint.post('')
def create_user():
    params = request.json
    user = User(**params)
    id = user_service.create_user(user)
    user.id = id
    return vars(user)


@blueprint.put('')
def update_user():
    params = request.json
    user = User(**params)
    user_service.update_user(user)
    return vars(user)


@blueprint.get('')
def get_all_users():
    users = user_service.get_users()
    return users


@blueprint.put('<string:id>/friends/<string:friend_id>')
def add_friend(id, friend_id):
    id, friend_id = int(id), int(friend_id)
    user_one = User(id=id)
    user_two = User(id=friend_id)
    user_service.add_friend(user_one, user_two)
    return {"result": "ok"}, 200


@blueprint.delete('/<string:id>/friends/<string:friend_id>')
def delete_friend(id, friend_id):
    id, friend_id = int(id), int(friend_id)
    user_one = User(id=id)
    user_two = User(id=friend_id)
    user_service.delete_friend(user_one, user_two)
    return {"result": "ok"}, 200


@blueprint.get('/<string:id>/friends')
def get_friends_of_user(id):
    id = int(id)
    user = User(id=id)
    friends = user_service.get_friends_of_user(user)
    return friends


@blueprint.get('/<string:id>/friends/common/<string:other_id>')
def get_common_friends(id, other_id):
    id, other_id = int(id), int(other_id)
    user_one = User(id=id)
    user_two = User(id=other_id)
    common_friends = user_service.get_common_friends(user_one, user_two)
    return common_friends


@blueprint.get('/<string:id>')
def get_user_by_id(id):
    id = int(id)
    user = User(id=id)
    get_user = user_service.get_user_by_id(user)
    return get_user, 200
