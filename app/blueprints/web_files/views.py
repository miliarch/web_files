from flask import redirect, render_template, current_app, url_for, abort
from pathlib import Path
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


@web_files.route('/debug')
def debug():
    return render_template('web_files/debug.html')
