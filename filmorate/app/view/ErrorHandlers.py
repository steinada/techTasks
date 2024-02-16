from flask import Blueprint
from filmorate.app.service.Errors import InsertionError


blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Exception)
def handle404(e):
    if isinstance(e, InsertionError):
        return {"error": e.message}, e.status_code

