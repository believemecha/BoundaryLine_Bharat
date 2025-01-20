from flask import Blueprint

playersBP = Blueprint('players', __name__, template_folder='../templates')


from . import routes
