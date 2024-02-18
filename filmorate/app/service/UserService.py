from datetime import datetime
from filmorate.app.repository.UserRepository import UserRepository
from filmorate.model.User import User
from filmorate.app.service.Errors import InsertionError
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
            created_users_list = list(map(lambda x: x[0], created_users))
            for obj in user_objs:
                if obj.id < 0:
                    logging.error(f"User {obj.id} is incorrect")
                    raise InsertionError("user id is incorrect", 404)
                if obj.id not in created_users_list:
                    logging.error(f"User {obj.id} not found")
                    raise InsertionError("user not created", 404)
            return func(self, *objs)
        return wrapper

    @staticmethod
    def make_user_json(users):
        keys = ('id', 'email', 'login', 'name', 'birthday')
        users_list = [dict(zip(keys, user)) for user in users]
        for user in users_list:
            user['birthday'] = str(datetime.fromisoformat(user['birthday']).date())
        return users_list

    @user_validator
    def create_user(self, user):
        birthday_date = datetime.fromisoformat(user.birthday)
        params = (user.email, user.login, user.name, birthday_date)
        id = self.user_repository.add_user(params)
        logging.info(f"User created: id={id}, {str(vars(user))}")
        return id

    @id_validator
    @user_validator
    def update_user(self, user):
        birthday_date = datetime.fromisoformat(user.birthday)
        params = (user.email, user.login, user.name, birthday_date, user.id)
        self.user_repository.update_user(params)
        logging.info(f"User updated: {str(vars(user))}")

    def get_users(self):
        users = self.user_repository.get_users()
        users_list = UserService.make_user_json(users)
        return users_list

    @id_validator
    def add_friend(self, user_one, user_two):
        self.user_repository.add_friend(user_one.id, user_two.id)

    @id_validator
    def delete_friend(self, user_one, user_two):
        self.user_repository.delete_friend(user_one.id, user_two.id)

    @id_validator
    def get_friends_of_user(self, user):
        friends_list = self.user_repository.get_friends_of_user(user.id)
        users_list = UserService.make_user_json(friends_list)
        return users_list

    @id_validator
    def get_common_friends(self, user_one, user_two):
        user_one_friends = self.user_repository.get_friends_of_user(user_one.id)
        user_two_friends = self.user_repository.get_friends_of_user(user_two.id)
        common_friends = set(user_one_friends) & set(user_two_friends)
        common_friends_list = UserService.make_user_json(common_friends)
        return common_friends_list

    @id_validator
    def get_user_by_id(self, user):
        user_req = self.user_repository.get_user_by_id(user.id)
        user_json = UserService.make_user_json(user_req)
        return user_json[0]
