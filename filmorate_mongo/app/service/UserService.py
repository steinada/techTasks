from datetime import datetime
from filmorate_mongo.app.repository.UserRepository import UserRepository
from filmorate_mongo.model.User import User
from filmorate_mongo.model.FriendshipStatus import FriendshipStatus
from filmorate_mongo.app.service.Errors import InsertionError
import logging


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    @staticmethod
    def user_validator(func):
        def wrapper(self, obj):
            if (obj.email is None) or ('@' not in obj.email):
                logging.error(f"Email {obj.email} is not valid")
                raise InsertionError("email error", 400)
            if obj.login is None or ' ' in obj.login:
                logging.error(f"Login {obj.login} is not valid")
                raise InsertionError("login error", 400)
            if obj.name is None or obj.name == "":
                obj.name = obj.login
            if datetime.fromisoformat(obj.birthday) > datetime.now():
                logging.error(f"Birthday {obj.birthday} is future date")
                raise InsertionError("birthday error", 400)
            return func(self, obj)
        return wrapper

    @staticmethod
    def id_validator(func):
        def wrapper(self, *objs):
            user_objs = filter(lambda x: isinstance(x, User), objs)
            created_users = UserRepository.get_created_users()
            created_users_list = list(map(lambda x: x['id'], created_users))
            for obj in user_objs:
                if obj.id < 0:
                    logging.error(f"User {obj.id} is incorrect")
                    raise InsertionError("user id is incorrect", 404)
                if obj.id not in created_users_list:
                    logging.error(f"User {obj.id} not found")
                    raise InsertionError("user not created", 404)
            return func(self, *objs)
        return wrapper

    @user_validator
    def create_user(self, user):
        params = vars(user)
        params['id'] = self.user_repository.id_generator()
        object_id = str(self.user_repository.add_user(params))
        logging.info(f"User created: object_id={object_id}, {str(params)}")
        del params['_id']
        return params

    @id_validator
    @user_validator
    def update_user(self, user):
        params = vars(user)
        user_updated = self.user_repository.update_user(params, user.id)
        logging.info(f"User updated: {str(vars(user))}")

    def get_users(self):
        users = self.user_repository.get_users()
        users_list = list(map(lambda x: x, users))
        return users_list

    @id_validator
    def add_friend(self, user_one, user_two):
        user_one_id, user_two_id = user_one.id, user_two.id
        self.user_repository.add_friend(user_one_id, user_two_id)

    @id_validator
    def delete_friend(self, user_one, user_two):
        self.user_repository.delete_friend(user_one.id, user_two.id)

    @id_validator
    def get_friends_of_user(self, user):
        friends_list = self.user_repository.get_friends_of_user(user.id)
        users_list = list(map(lambda x: x['friends_info'][0], friends_list))
        return users_list

    @id_validator
    def get_common_friends(self, user_one, user_two):
        friends = self.user_repository.get_common_friends(user_one.id, user_two.id)
        friends_dict, users_list, common_friends = dict(), list(), list()
        for friend in friends:
            friends_dict[(friend['_id'], friend['friends_info'][0]['id'])] = friend['friends_info'][0]
        for user in friends_dict:
            if user[1] in users_list:
                common_friends.append(friends_dict[user])
            users_list.append(user[1])
        return common_friends

    @id_validator
    def get_user_by_id(self, user):
        user = self.user_repository.get_user_by_id(user.id)
        return user
