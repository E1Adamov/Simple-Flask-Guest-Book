import pytest

from app import app
import config

data_set = [
    (True, '200 OK', None, None, None),
    (True, '200 OK', {'unexpected_param': 'unexpected'}, None, None),
    (True, '200 OK', None, {'Accept': 'unknown mime type'}, None),
    (True, '200 OK', None, None, {'unexpected data': "unexpected"}),
    (False, '200 OK', None, None, None),
]


@pytest.mark.parametrize('follow_redirects, expected_response_code, query_string, headers, data', data_set)
def test_render_message_board(follow_redirects, expected_response_code, query_string, headers, data):
    kwargs = {k: v for k, v in locals().items() if k != 'expected_response_code' and v is not None}
    kwargs['path'] = f'/{config.URL_BOARD}'

    client = app.test_client()

    print('Test GET', kwargs)
    response = client.get(**kwargs)

    assert response.status == expected_response_code
    assert response.mimetype == 'text/html'
    assert response.charset == 'utf-8'
