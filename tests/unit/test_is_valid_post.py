import string

import pytest

from tests import helpers


class Red:
    def __init__(self, string_):
        self.string = string_

    def __str__(self):
        return self.string


data_set = [
    (string.printable, True),
    ('', True),
    ("'", True),
    ('"', True),
    (' ', True),
    ('RE+D ', True),
    ('R,ED ', True),
    (r'Valid red te\xtredtext', True),
    ('Vali/d Red textrEDtext', True),
    ('Valid RE D text"RE Dtext', True),
    ('Valid DRE }textRE Dtext', True),
    (u'Valid uni(code text', True),
    ('рэд ё', True),
    ('ÅÆØ', True),
    ('%D0%81', True),

    ('Invalid encoding'.encode('latin'), False),
    (b'Bytes', False),
    (None, False),
    ('"RED"', False),
    ("'RED'", False),
    (u'RED', False),
    (b'RED', False),
    ('xxREDxx', False),
    (' RED', False),
    ('RED ', False),
    (' RED ', False),
    ('REDRED', False),
    ('\RED', False),
    ('\\RED', False),
    (Red('RED'), False),
   (Red('Blue'), False),
]


@pytest.mark.parametrize('message, expected_result', data_set)
def test_is_valid_post(message, expected_result):
    print('Test message', message)
    assert helpers.is_valid_message(message) == expected_result
