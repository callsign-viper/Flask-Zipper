import gzip
import zlib

import brotli
from unittest import TestCase
from flask import Flask
from flask.testing import FlaskClient

from flask_zipper import *


def _decode_response_data_with_brotli(response):
    return brotli.decompress(response.data).decode()


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

    def _test_encoded_response(self, client, content_encoding_string, decoder_function):
        resp = client.get('/', headers={'Accept-Encoding': content_encoding_string})
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.headers['Content-Encoding'], content_encoding_string)
        self.assertEqual(resp.headers['Vary'], 'Accept-Encoding')

        self.assertEqual(decoder_function(resp), self.response_message)

    def _test_content_encoding_header_missing(self, client):
        resp = client.get('/')
        self.assertEqual(resp.status_code, 200)

        self.assertNotIn('Content-Encoding', resp.headers)

        self.assertEqual(resp.data.decode(), self.response_message)

    def _test_content_encoding_value_missing(self, client):
        resp = client.get('/', headers={'Accept-Encoding': 'foo'})
        self.assertEqual(resp.status_code, 200)

        self.assertNotIn('Content-Encoding', resp.headers)

        self.assertEqual(resp.data.decode(), self.response_message)


class TestBrotli(BaseTestCase):
    def setUp(self):
        super(TestBrotli, self).setUp()
        
        self.target_func = encode_brotli
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func)

    def test(self):
        self._test_encoded_response(self.client, 'br', _decode_response_data_with_brotli)
        self._test_content_encoding_header_missing(self.client)
        self._test_content_encoding_value_missing(self.client)
