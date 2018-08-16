import gzip
import zlib

import brotli
from unittest import TestCase
from flask import Flask
from flask.testing import FlaskClient

from flask_zipper import *


def decode_response_data_with_brotli(response):
    return brotli.decompress(response.data).decode()


def decode_response_data_with_deflate(response):
    return zlib.decompress(response.data).decode()


def decode_response_data_with_gzip(response):
    return gzip.decompress(response.data).decode()


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


CONTENT_ENCODING_STRING_DECORATOR_DECODER_MAPPING = {
    'br': (encode_brotli, decode_response_data_with_brotli),
    'deflate': (encode_deflate, decode_response_data_with_deflate),
    'gzip': (encode_gzip, decode_response_data_with_gzip)
}


def _test_all(content_encoding_string):
    target_func, decoder_function = CONTENT_ENCODING_STRING_DECORATOR_DECODER_MAPPING[content_encoding_string]

    client = get_test_client_of_decorated_view_function_registered_flask_app(target_func)

    _test_encoded_response(client, content_encoding_string, decoder_function)
    _test_content_encoding_header_missing(client)
    _test_content_encoding_value_missing(client)


def test_brotli():
    _test_all('br')


def test_deflate():
    _test_all('deflate')


def test_gzip():
    _test_all('gzip')
