from functools import wraps

from flask import after_this_request

from flask_zipper.compressor import *
from flask_zipper.exceptions import *
from flask_zipper.util import get_zipper


def _get_decorator(kwargs_dict):
    """
    A function to make specific decorator

    :param kwargs_dict: encode_response argument
    :return: specific decorator
    """
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
    'compress_function': encode_response_data_with_brotli,
    'error_class': BrotliCompressionError
})  #: brotli encoder decorator


encode_deflate = _get_decorator({
    'accept_encoding_string': 'deflate',
    'compress_function': encode_response_data_with_deflate,
    'error_class': DeflateCompressionError
})  #: deflate encoder decorator


encode_gzip = _get_decorator({
    'accept_encoding_string': 'gzip',
    'compress_function': encode_response_data_with_gzip,
    'error_class': GzipCompressionError
})  #: gzip encoder decorator
