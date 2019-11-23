import os

import pytest

from app import app
from tests import helpers
import config

data_set = [
    ('postMessage.js', '200 OK', 'application/javascript', None, None, None),
    ('PostmeSSage.js', '200 OK', 'application/javascript', {'unexpected_param': 'unexpected'}, None, None),
    ('PostmeSSage.js', '200 OK', 'application/javascript', None, {'Content-Type': 'image/x-icon', 'charset': 'ISO-8859-1'}, None),
    ('PostmeSSage.js', '200 OK', 'application/javascript', None, None, {'Surprise': "<h1>HELLO</h1>"}),
    (u'PostmeSSage.js', '200 OK', 'application/javascript', None, None, None),
    (bytes('PostmeSSage.js'.encode('latin')), '200 OK', 'application/javascript', None, None, None),
    ('postMessage.js#', '200 OK', 'application/javascript', None, None, None),

    ('postMessage.js ', '404 NOT FOUND', 'text/html', None, None, None),
    ('postMessage.js/', '404 NOT FOUND', 'text/html', None, None, None),
    ('nonExisting.js', '404 NOT FOUND', 'text/html', None, None, None),
    ('postMessage,js', '404 NOT FOUND', 'text/html', None, None, None),
    ('postMessage..js', '404 NOT FOUND', 'text/html', None, None, None),
    ('postMessage;js', '404 NOT FOUND', 'text/html', None, None, None),
    ('js/postMessage.js', '404 NOT FOUND', 'text/html', None, None, None),
    (r'js\postMessage.js', '404 NOT FOUND', 'text/html', None, None, None),
]


def get_expected_file_length(file_name):
    if isinstance(file_name, bytes):
        file_name = file_name.decode('latin')

    file_name = file_name.replace('#', '')

    js_file_path = os.path.join(helpers.get_server_path(), config.PATH_JS, file_name)

    with open(js_file_path, 'rb') as f:
        js_file = f.read()
        return len(js_file)


@pytest.mark.parametrize('path, expected_status, expected_mime_type, query_string, headers, data', data_set)
def test_send_js(path, expected_status, expected_mime_type, query_string, headers, data):

    kwargs = {k: v for k, v in locals().items() if k not in ['expected_status', 'expected_mime_type'] and v is not None}
    client = app.test_client()

    print('Test GET', kwargs)
    response = client.get(**kwargs)

    assert response.status == expected_status
    assert response.mimetype == expected_mime_type
    assert response.charset == 'utf-8'
    assert response.content_length == len(response.data)

    if expected_status == '200 OK':
        assert get_expected_file_length(kwargs['path']) == len(response.data)
