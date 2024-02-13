from flask import Blueprint


blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Exception)
def handle404(e):
    return '404 handled'

