import pytest
from pathlib import Path
from app import create_app


@pytest.fixture()
def web_root():
    return Path(__file__).parent.joinpath('data/web_root')


@pytest.fixture()
def app(web_root):
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'TESTING',
        'SITE_TITLE': 'Web File Manager',
        'WEB_FILES_WEB_ROOT': web_root,
        'WEB_FILES_DOMAIN_ROOT': 'http://localhost:5001'
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
