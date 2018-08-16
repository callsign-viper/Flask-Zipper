import gzip
import zlib

import brotli
from unittest import TestCase
from flask import Flask
from flask.testing import FlaskClient

from flask_zipper import *


class BaseTestCase(TestCase):
    def setUp(self):
        self.response_message = 'hello'

    def tearDown(self):
        pass

    def _get_test_client_of_decorated_view_function_registered_flask_app(self, decorator_func) -> FlaskClient:
        def view_func():
            return 'hello'

        decorated_view_func = decorator_func(view_func)
        app = Flask(__name__)
        Zipper(app)

        app.add_url_rule('/', view_func=decorated_view_func)

        return app.test_client()

    def _test_encoded_response(self, client, accept_encoding_string, decoder_function):
        resp = client.get('/', headers={'Accept-Encoding': accept_encoding_string})
        self.assertEqual(resp.status_code, 200)

        print(resp.headers)
        self.assertEqual(resp.headers['Content-Encoding'], accept_encoding_string)
        self.assertEqual(resp.headers['Vary'], 'Accept-Encoding')

        self.assertEqual(decoder_function(resp), self.response_message)

