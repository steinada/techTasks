from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from what_to_watch.settings import Config

app = Flask(__name__)
app.json.ensure_ascii = False
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from what_to_watch.opinions_app import api_views, cli_commands, error_handlers, views
