from flask import redirect, url_for
from app import app


@app.route("/")
def index():
    return redirect(url_for('web_files.file_manager_index'))
