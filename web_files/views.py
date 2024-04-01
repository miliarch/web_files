from flask import redirect, render_template
from pathlib import Path
from . import app


def list_directory_contents(path, pattern='*'):
    return list(Path(path).rglob(pattern))


@app.route("/")
def file_manager():
    files = list_directory_contents('/tmp/web_files/')
    return render_template('file_manager.html', files=files)


@app.route('/debug')
def debug():
    return render_template('debug.html')
