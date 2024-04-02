from flask import redirect, render_template
from pathlib import Path
from app.blueprints.web_files import web_files


def list_directory_contents(path, pattern='*'):
    return list(Path(path).rglob(pattern))


@web_files.route("/")
def file_manager():
    files = list_directory_contents('/var/www')
    return render_template('web_files/file_manager.html', files=files)


@web_files.route('/debug')
def debug():
    return render_template('web_files/debug.html')
