from flask import Flask
from app.blueprints.web_files import web_files


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.register_blueprint(web_files, url_prefix='/')
    return app
