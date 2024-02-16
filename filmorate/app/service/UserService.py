from datetime import datetime
from filmorate.app.repository.UserRepository import UserRepository
from filmorate.app.service.Errors import InsertionError
import logging


class UserService:

    @staticmethod
    def user_validator(func):
        def wrapper(obj):
            if (obj.email is None) or ('@' not in obj.email):
                logging.error(f"Email {obj.email} is not valid")
                raise InsertionError("email error", 400)
            if obj.login is None or ' ' in obj.login:
                logging.error(f"Login {obj.login} is not valid")
                raise InsertionError("login error", 400)
            if obj.name is None:
                obj.name = obj.login
            if datetime.fromisoformat(obj.birthday) > datetime.now():
                logging.error(f"Birthday {obj.birthday} is future date")
                raise InsertionError("birthday error", 400)
            return func(obj)
        return wrapper

    @staticmethod
    def id_validator(func):
        def wrapper(obj):
            created_users = UserRepository.get_created_users()
            created_users_list = list(map(lambda x: x[0], created_users))
            if obj.id not in created_users_list:
                logging.error(f"User {obj.id} not found")
                raise InsertionError("user not created", 404)
            return func(obj)
        return wrapper

    @staticmethod
    @user_validator
    def create_user(user):
        birthday_date = datetime.fromisoformat(user.birthday)
        params = (user.email, user.login, user.name, birthday_date)
        id = UserRepository.add_user(params)
        logging.info(f"User created: id={id}, {str(vars(user))}")
        return id

    @staticmethod
    @id_validator
    @user_validator
    def update_user(user):
        birthday_date = datetime.fromisoformat(user.birthday)
        params = (user.email, user.login, user.name, birthday_date, user.id)
        UserRepository.update_user(params)
        logging.info(f"User updated: {str(vars(user))}")

    @staticmethod
    def get_users():
        users = UserRepository.get_users()
        keys = ('id', 'email', 'login', 'name', 'birthday')
        users_list = [dict(zip(keys, user)) for user in users]
        for user in users_list:
            user['birthday'] = str(datetime.fromisoformat(user['birthday']).date())
        return users_list
