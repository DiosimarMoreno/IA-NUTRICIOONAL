from flask import Blueprint

nutritionist_bp = Blueprint('nutritionist', __name__, template_folder='templates')

from . import routes