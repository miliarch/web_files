from flask import Blueprint

site = Blueprint(
    'site',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from web_files.blueprints.site import views
