from flask import Flask
from web_files.site import site


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.register_blueprint(site, url_prefix='/')
    return app
