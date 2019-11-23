import string

import pytest

import config
from tests.base_test import base_test
from tests import helpers
from app import app


data_set = [
    ('George', 'Hiya', '200 OK', None, None, True),

    ('Veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeery\n'
     'looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong\n'
     'naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaame',
     'Hiya', '200 OK', None, None, True),

    ('Noise in url', 'Hiya', '200 OK', {'unexpected_param': 'unexpected'}, None, True),
    ('Invalid headers', 'Hiya', '200 OK', None, {'Accept': 'unknown mime type'}, True),
    ('рэд ё \ÅÆØ %D0%81', string.printable, '200 OK', None, {'Accept': 'unknown mime type'}, True),
    ('SQL injection attempt', ' UNION SELECT message FROM message_board--; DROP TABLE message_board;', '200 OK', None, {'Accept': 'unknown mime type'}, True),

    ('No redirects', 'Hiya', '302 FOUND', None, None, False),

    ('Invalid substring', 'RED Hiya', '403 FORBIDDEN', None, None, True),
    ('Only whitespace', ' ', '403 FORBIDDEN', None, None, True),
    ('Empty', '', '403 FORBIDDEN', None, None, True),
    ('Obviously, too long', '$' * 32000, '403 FORBIDDEN', None, None, True),
]


@pytest.mark.parametrize('name, message, expected_response_code, query_string, headers, follow_redirects', data_set)
def test_post_a_message(base_test, name, message, expected_response_code, query_string, headers, follow_redirects):
    kwargs = {k: v for k, v in locals().items() if k not in ['name', 'message', 'expected_response_code'] and v is not None}
    new_post = {'name': name, 'message': message}
    kwargs['data'] = new_post
    kwargs['path'] = config.URL_SUBMIT

    expected_posts = helpers.get_posts()

    client = app.test_client()

    print('Test post a message:', kwargs)
    response = client.post(**kwargs)

    assert response.status == expected_response_code
    assert response.mimetype == 'text/html'
    assert response.charset == 'utf-8'

    if int(expected_response_code.split()[0]) < 400:
        expected_posts.append(new_post)

    actual_posts = helpers.get_posts()

    assert expected_posts == actual_posts
