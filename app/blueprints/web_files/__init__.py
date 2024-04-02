from flask import Blueprint

web_files = Blueprint(
    'web_files',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from app.blueprints.web_files import views
