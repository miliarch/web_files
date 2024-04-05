from datetime import datetime
from flask import redirect, render_template, current_app, url_for, abort, request, flash, jsonify
from pathlib import Path
from werkzeug.utils import secure_filename
from app.blueprints.web_files import web_files


def list_directory_contents(path, pattern='*'):
    return list(Path(path).glob(pattern))


@web_files.app_template_filter('generate_parent_web_root_relative_path')
def generate_parent_web_root_relative_path(path):
    relative_path = Path(generate_web_root_relative_path(path))
    if len(relative_path.parents) > 1:
        return relative_path.parents[1]
    return '.'


@web_files.app_template_filter('generate_web_root_relative_path')
def generate_web_root_relative_path(path):
    web_root = Path(current_app.config['WEB_FILES_WEB_ROOT'])
    return '/'.join(Path(path).parts[len(web_root.parts):])


@web_files.app_template_filter('generate_full_directory_path')
def generate_full_directory_path(directory):
    web_root = Path(current_app.config['WEB_FILES_WEB_ROOT'])
    full_path = web_root.joinpath(directory)
    if not full_path.exists():
        abort(404)
    return full_path


@web_files.app_template_filter('generate_domain_root_url')
def generate_domain_root_url(file):
    domain_root = current_app.config['WEB_FILES_DOMAIN_ROOT']
    return f'{domain_root}/{generate_web_root_relative_path(file)}'


@web_files.app_template_filter('format_file_mtime')
def format_file_mtime(mtime):
    dt = datetime.utcfromtimestamp(mtime)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


@web_files.route('/')
def file_manager_index():
    return redirect(url_for('web_files.file_manager_browse', directory='.'))


@web_files.route('/browse/')
@web_files.route('/browse/<path:directory>')
def file_manager_browse(directory='.'):
    # validate user provided path
    full_path = generate_full_directory_path(directory)
    files = list_directory_contents(full_path, '*')

    # sort files by filename (stem) alphabetically in ascending order
    files.sort(key=lambda x: x.stem)

    # sort directories before files
    # False == 0, True == 1, thus True orders after False ascending
    files.sort(key=lambda x: x.is_file())

    return render_template(
        'web_files/file_manager.html',
        directory=directory,
        files=files,
    )


@web_files.route('/upload', methods=['POST'])
def file_manager_upload():
    directory = request.form.get('directory')

    if not directory:
        current_app.logger.debug(f'directory provided: {directory}')
        flash('No directory provided')
        return redirect(url_for('web_files.file_manager_browse', directory='.'))

    if 'file' not in request.files:
        flash('No file in request')
        return redirect(url_for('web_files.file_manager_browse', directory=directory))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('web_files.file_manager_browse', directory=directory))

    filename = secure_filename(file.filename)
    base_path = generate_full_directory_path(directory)
    if file and base_path.exists():
        full_path = base_path.joinpath(filename)
        file.save(full_path)

    # redirect to previous directory
    return redirect(url_for('web_files.file_manager_browse', directory=directory))


@web_files.route('/delete', methods=['DELETE'])
def file_manager_delete():
    payload = request.get_json()
    path = Path(payload['path'])
    directory = Path(payload['directory'])
    full_path = generate_full_directory_path(path)

    if full_path.is_dir():
        try:
            full_path.rmdir()
            flash(f'Directory "{path}" removed successfully')
        except IOError:
            flash(f'Directory "{path}" must be empty before it can be deleted')
    else:
        try:
            full_path.unlink(missing_ok=False)
            flash(f'File "{path}" removed successfully')
        except IOError:
            flash(f'Error accessing file "{path}"')
        except FileNotFoundError:
            flash(f'File "{path}" does not exist')

        response = {
            'redirect': url_for('web_files.file_manager_browse', directory=directory)
        }

    return jsonify(response)


@web_files.route('/debug')
def debug():
    return render_template('web_files/debug.html')
