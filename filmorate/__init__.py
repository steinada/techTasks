from flask import Flask
import filmorate.app.view.FilmController
import filmorate.app.view.UserController
import filmorate.app.view.ErrorHandlers
import filmorate.app.view.GenreController
import filmorate.app.view.MpaController
import filmorate.app.view.DirectorController


f_app = Flask(__name__)
f_app.json.ensure_ascii = False

f_app.register_blueprint(filmorate.app.view.FilmController.blueprint, url_prefix='/films')
f_app.register_blueprint(filmorate.app.view.UserController.blueprint, url_prefix='/users')
f_app.register_blueprint(filmorate.app.view.GenreController.blueprint, url_prefix='/genres')
f_app.register_blueprint(filmorate.app.view.MpaController.blueprint, url_prefix='/mpa')
f_app.register_blueprint(filmorate.app.view.DirectorController.blueprint, url_prefix='/directors')
f_app.register_blueprint(filmorate.app.view.ErrorHandlers.blueprint)


if __name__ == '__main__':
    f_app.run(host='localhost', port=8080)

