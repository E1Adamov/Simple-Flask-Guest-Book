import pytest

from app import app
import config

data_set = [
    ({'name': "<h1>HELLO</h1", 'message': 'REqD'}, True, '200 OK', None, None),
    ({'name': "RED'", 'message': 'REq"D'}, True, '200 OK', {'unexpected_param': 'unexpected'}, None),
    ({'name': "my name'", 'message': 'REq"D'}, True, '200 OK', None, {'Accept': 'unknown mime type'}),
    ({'name': "my na;{([me'", 'message': 'R;)}]Eq"D'}, True, '200 OK', None, None),
    ({'name': r"рэд ё \ÅÆØ %D0%81", 'message': '/'}, True, '200 OK', None, None),
    ({'name': r"my name1", 'message': ' UNION SELECT name FROM message_board--'}, True, '200 OK', None, None),
    ({'name': "<h1>HELLO</h1".encode('latin'), 'message': b'REqD'}, True, '200 OK', None, None),

    ({'name': "my name", 'message': 'my message'}, False, '302 FOUND', None, None),

    ({'name': "", 'message': 'hello'}, True, '403 FORBIDDEN', None, None),
    ({'name': "name", 'message': ' '}, True, '403 FORBIDDEN', None, None),
    ({'name': "\n", 'message': '\n'}, True, '403 FORBIDDEN', None, None),
    ({'name': "my name", 'message': 'RED'}, True, '403 FORBIDDEN', None, None),
    ({'name': "That's too long", 'message': '$' * 32000}, True, '403 FORBIDDEN', None, None),

    ({'new_column': "my name", 'message': 'my message'}, True, '400 BAD REQUEST', None, None),
    ({'Name': "my name", 'Message': 'my message'}, False, '400 BAD REQUEST', None, None),
]


@pytest.mark.parametrize('data, follow_redirects, expected_response_code, query_string, headers', data_set)
def test_submit_message(data, follow_redirects, expected_response_code, query_string, headers):
    kwargs = {k: v for k, v in locals().items() if k != 'expected_response_code' and v is not None}
    kwargs['path'] = f'/{config.URL_SUBMIT}'

    client = app.test_client()

    print('Test POST', kwargs)
    response = client.post(**kwargs)

    assert response.status == expected_response_code
    assert response.mimetype == 'text/html'
    assert response.charset == 'utf-8'
