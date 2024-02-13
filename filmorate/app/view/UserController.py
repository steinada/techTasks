from flask import request, Blueprint
from filmorate.app.service.UserService import UserService
# from flask_classy import FlaskView, route
from filmorate.model.User import User


blueprint = Blueprint('users', __name__)
user_service = UserService()


# class UserController(FlaskView):
#     user_service = UserService()

@blueprint.route('', methods=['POST'])
def create_user():
    params = request.json
    user = User(**params)
    id = user_service.create_user(user)
    user.id = id
    return vars(user)


@blueprint.route('', methods=['PUT'])
def update_user():
    params = request.json
    user = User(**params)
    user_service.update_user(user)
    return vars(user)


@blueprint.route('', methods=['GET'])
def get_all_users():
    users = user_service.get_users()
    return users

    # @errorhandler(Exception)
    # def error(self):
    #     return 400
