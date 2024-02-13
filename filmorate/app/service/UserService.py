from datetime import datetime
from filmorate.app.repository.UserRepository import UserRepository
from filmorate.app.service.Errors import InsertionError


class UserService:

    @staticmethod
    def user_validator(func):
        def wrapper(obj):
            if (obj.email is None) or ('@' not in obj.email):
                raise AssertionError
            if obj.login is None or ' ' in obj.login:
                raise InsertionError("login error", 400)
            if obj.name is None:
                obj.name = obj.login
            if datetime.fromisoformat(obj.birthday) > datetime.now():
                raise InsertionError("birthday error", 400)
            return func(obj)
        return wrapper

    @staticmethod
    @user_validator
    def create_user(user):
        birthday_date = datetime.fromisoformat(user.birthday)
        params = (user.email, user.login, user.name, birthday_date)
        id = UserRepository.add_user(params)
        return id

    @staticmethod
    @user_validator
    def update_user(user):
        birthday_date = datetime.fromisoformat(user.birthday)
        params = (user.email, user.login, user.name, birthday_date, user.id)
        UserRepository.update_user(params)

    @staticmethod
    def get_users():
        users = UserRepository.get_users()
        keys = ('id', 'email', 'login', 'name', 'birthday')
        users_list = [dict(zip(keys, user)) for user in users]
        for user in users_list:
            user['birthday'] = str(datetime.fromisoformat(user['birthday']).date())
        return users_list
