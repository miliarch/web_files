import json


def test_get_response_code_index(client):
    response = client.get('/files/')
    assert response.status_code == 302
    assert response.location == '/files/browse/.'
    response = client.get('/')


def test_get_response_code_browse(client):
    response = client.get('/files/browse')
    assert response.status_code == 308
    assert response.location == 'http://localhost/files/browse/'


def test_get_response_code_browse_base(client):
    response = client.get('/files/browse/')
    assert response.status_code == 200


def test_get_response_code_browse_dir1(client, web_root):
    query_dir = web_root.joinpath('dir1')
    if not query_dir.exists():
        query_dir.mkdir()
    assert query_dir.exists
    response = client.get('/files/browse/dir1')
    assert response.status_code == 200
    query_dir.rmdir()
    assert not query_dir.exists()


def test_upload_success(client, web_root):
    # Scaffold test
    source_file = web_root.joinpath('file1.txt')
    if not source_file.exists():
        source_file.write_bytes(b'hello tester')
    dest_file = web_root.joinpath('dir1/file1.txt')
    if not dest_file.parent.exists():
        # dir has to exist before file is written to it
        dest_file.parent.mkdir()
    if dest_file.exists():
        dest_file.unlink()
    expected_flash_message = f'File {source_file.name} uploaded successfully'

    # Assert scaffolding
    assert source_file.exists()
    assert not dest_file.exists()

    # Execute test
    with open(source_file, 'rb') as f:
        data = {
            'directory': 'dir1',
            'file': (f, source_file.name),
        }
        response = client.post(
            '/files/upload',
            data=data,
            follow_redirects=False,
        )

    # Inspect results
    with client.session_transaction() as session:
        assert 'success' in dict(session['_flashes'])
        flash_message = dict(session['_flashes']).get('success')
        assert flash_message == expected_flash_message

    assert response.status_code == 302
    assert response.location == '/files/browse/dir1'
    assert dest_file.exists()
    assert source_file.read_bytes() == dest_file.read_bytes()

    # Clean up
    dest_file.unlink()
    dest_file.parent.rmdir()
    source_file.unlink()
    assert not dest_file.exists()
    assert not dest_file.parent.exists()
    assert not source_file.exists()


def test_delete_file_success(client, web_root):
    # Scaffold test
    file = web_root.joinpath('testdel.txt')
    if file.exists():
        file.unlink()
    assert not file.exists()
    expected_flash_message = f'File "{file.name}" removed successfully'

    # Create test file
    with file.open('wb') as f:
        f.write(b'test')
    assert file.exists()
    assert file.read_bytes() == b'test'

    # Execute test
    data = {
        'directory': '.',
        'path': file.name,
    }
    response = client.delete(
        '/files/delete',
        data=json.dumps(data),
        content_type='application/json',
        follow_redirects=False,
    )

    # Inspect results
    with client.session_transaction() as session:
        flash_message = dict(session['_flashes']).get('success')
        assert flash_message == expected_flash_message

    assert response.status_code == 200
    assert not file.exists()


def test_create_success(client, web_root):
    # Scaffold test
    dest_dir = web_root.joinpath('testdir')
    if dest_dir.exists():
        dest_dir.rmdir()
    expected_flash_message = f'Directory "{dest_dir}" created successfully'

    # Assert scaffolding
    assert not dest_dir.exists()

    # Execute test
    data = {
        'directory': '.',
        'name': dest_dir.name,
    }
    response = client.post(
        '/files/create',
        data=data,
        follow_redirects=False,
    )

    # Inspect results
    with client.session_transaction() as session:
        flash_message = dict(session['_flashes']).get('success')
        assert flash_message == expected_flash_message

    assert response.status_code == 302
    assert response.location == '/files/browse/.'
    assert dest_dir.exists()

    # Clean up
    dest_dir.rmdir()
    assert not dest_dir.exists()
