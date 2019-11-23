import pytest

from tests.server_handler import ServerHandler


@pytest.fixture(scope='session')
def base_test(request):

    print('tests\\unit' in request.node._pkg_roots)

    def abort_test():
        print('Aborting test')
        exit(-1)

    def teardown():
        if sh.server_was_started:
            sh.handle_server_at_teardown()

    sh = ServerHandler()

    server_status = sh.get_server_status()

    if server_status == 'off':
        sh.handle_server_at_startup()

    elif server_status == 'broken':
        abort_test()

    request.addfinalizer(teardown)
