from flask import Flask
import filmorate_mongo.app.view.FilmController
import filmorate_mongo.app.view.UserController
import filmorate_mongo.app.view.ErrorHandlers
import filmorate_mongo.app.view.GenreController
import filmorate_mongo.app.view.MpaController
import filmorate_mongo.app.view.DirectorController


f_app = Flask(__name__)
f_app.json.ensure_ascii = False

f_app.register_blueprint(filmorate_mongo.app.view.FilmController.blueprint, url_prefix='/films')
f_app.register_blueprint(filmorate_mongo.app.view.UserController.blueprint, url_prefix='/users')
f_app.register_blueprint(filmorate_mongo.app.view.GenreController.blueprint, url_prefix='/genres')
f_app.register_blueprint(filmorate_mongo.app.view.MpaController.blueprint, url_prefix='/mpa')
f_app.register_blueprint(filmorate_mongo.app.view.DirectorController.blueprint, url_prefix='/directors')
f_app.register_blueprint(filmorate_mongo.app.view.ErrorHandlers.blueprint)


if __name__ == '__main__':
    f_app.run(host='localhost', port=8080)

