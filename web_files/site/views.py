from flask import redirect, render_template
from pathlib import Path
from web_files.site import site


def list_directory_contents(path, pattern='*'):
    return list(Path(path).rglob(pattern))


@site.route("/")
def file_manager():
    files = list_directory_contents('/var/www')
    return render_template('file_manager.html', files=files)


@site.route('/debug')
def debug():
    return render_template('debug.html')
