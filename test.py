import gzip
import zlib

import brotli
from unittest import TestCase
from flask import Flask
from flask.testing import FlaskClient

from flask_zipper import *


def decode_response_data_with_brotli(response):
    return brotli.decompress(response.data).decode()


RESPONSE_MESSAGE = 'hello'


def get_test_client_of_decorated_view_function_registered_flask_app(decorator_func) -> FlaskClient:
    def view_func():
        return RESPONSE_MESSAGE

    decorated_view_func = decorator_func(view_func)
    app = Flask(__name__)
    Zipper(app)

    app.add_url_rule('/', view_func=decorated_view_func)

    return app.test_client()


def _test_encoded_response(client, content_encoding_string, decoder_function):
    resp = client.get('/', headers={'Accept-Encoding': content_encoding_string})
    assert resp.status_code == 200

    assert resp.headers['Content-Encoding'] == content_encoding_string
    assert resp.headers['Vary'] == 'Accept-Encoding'

    assert decoder_function(resp) == RESPONSE_MESSAGE


def _test_content_encoding_header_missing(client):
    resp = client.get('/')
    assert resp.status_code == 200

    assert 'Content-Encoding' not in resp.headers

    assert resp.data.decode() == RESPONSE_MESSAGE


def _test_content_encoding_value_missing(client):
    resp = client.get('/', headers={'Accept-Encoding': 'foo'})
    assert resp.status_code == 200

    assert 'Content-Encoding' not in resp.headers

    assert resp.data.decode() == RESPONSE_MESSAGE


def _test_all(target_func, content_encoding_string, decoder_function):
    client = get_test_client_of_decorated_view_function_registered_flask_app(target_func)

    _test_encoded_response(client, content_encoding_string, decoder_function)
    _test_content_encoding_header_missing(client)
    _test_content_encoding_value_missing(client)


def test_brotli():
    _test_all(encode_brotli, 'br', decode_response_data_with_brotli)
