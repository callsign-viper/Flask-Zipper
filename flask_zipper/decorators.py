from functools import wraps

from flask import after_this_request

from flask_zipper.compressor import *
from flask_zipper.exceptions import *
from flask_zipper.util import get_zipper


def _get_decorator(kwargs_dict):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            @after_this_request
            def zipper(response):
                kwargs_dict['response'] = response

                return get_zipper().encode_response(**kwargs_dict)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


encode_brotli = _get_decorator({
    'accept_encoding_string': 'br',
    'compressor': encode_response_with_brotli,
    'error_class': BrotliCompressionError
})


encode_deflate = _get_decorator({
    'accept_encoding_string': 'deflate',
    'compressor': encode_response_with_deflate,
    'error_class': DeflateCompressionError
})


encode_gzipped = _get_decorator({
    'accept_encoding_string': 'gzip',
    'compressor': encode_response_with_gzip,
    'error_class': GzipCompressionError
})
