import os
import subprocess
import time

import requests

import config
from tests import helpers


class ServerHandler:
    def __init__(self):
        self.__process = None
        self.server_was_started = False

    @property
    def server_was_started(self):
        return self.__server_was_started

    @server_was_started.setter
    def server_was_started(self, new_value):
        assert new_value in [True, False]
        self.__server_was_started = new_value

    @staticmethod
    def get_server_status():
        """
        :return: 'ok' if the server is OK
                 'off' if the server is OFF
                 'broken' if the server returns non-200 response
        """
        try:
            response = requests.get('http://{}:{}'.format(config.HOST_NAME, config.PORT))

        except requests.exceptions.ConnectionError:
            print("The server is off")
            return 'off'

        else:
            if response.ok:
                return 'ok'

            else:
                print("The server is broken", response.status_code)
                return 'broken'

    def handle_server_at_startup(self):
        print('Start the server')
        app_path = os.path.join(helpers.get_server_path(), config.APP_FILE_NAME)
        self.__process = subprocess.Popen(['python3', app_path])
        self.server_was_started = True
        time.sleep(3)

    def handle_server_at_teardown(self):
        print('Stop the server')
        try:
            self.__process.terminate()
        except Exception as e:
            print("Can't stop the server:", type(e), e)
