from flask import redirect, render_template, current_app, request, url_for, abort
from pathlib import Path
from app.blueprints.web_files import web_files


def list_directory_contents(path, pattern='*'):
    return list(Path(path).glob(pattern))

@web_files.route('/')
def file_manager_index():
    return redirect(url_for('web_files.file_manager_browse', directory='.'))


@web_files.route('/browse')
@web_files.route('/browse/<path:directory>')
def file_manager_browse(directory='.'):
    web_root = Path(current_app.config['WEB_FILES_WEB_ROOT'])
    full_path = web_root.joinpath(directory)
    if not full_path.exists():
        abort(404)

    files = list_directory_contents(full_path, '*')
    return render_template('web_files/file_manager.html', directory=directory, web_root=web_root, files=files)


@web_files.route('/debug')
def debug():
    return render_template('web_files/debug.html')
