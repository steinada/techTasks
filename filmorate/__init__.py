from flask import Flask
# from app import routes
import filmorate.app.view.FilmController
import filmorate.app.view.UserController
import filmorate.app.view.ErrorHandlers


f_app = Flask(__name__)
f_app.json.ensure_ascii = False
# f_app.register_blueprint(routes.app_blueprint_film)
# f_app.register_blueprint(routes.app_blueprint_user)

f_app.register_blueprint(filmorate.app.view.FilmController.blueprint, url_prefix='/films')
f_app.register_blueprint(filmorate.app.view.UserController.blueprint, url_prefix='/users')
f_app.register_blueprint(filmorate.app.view.ErrorHandlers.blueprint)


if __name__ == '__main__':
    f_app.run(host='localhost', port=8080)

