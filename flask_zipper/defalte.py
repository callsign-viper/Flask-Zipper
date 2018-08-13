from functools import wraps
import zlib
from flask import after_this_request, request, current_app

from .exceptions import DeflateCompressionError
from .util import _get_zipper

def deflate_compress(response):
    response.data = zlib.compress(response.data, current_app.config['DEFLATE_COMPRESS_LEVEL'])
    response.headers.update({
        'Content-Encoding': 'defalte',
        'Vary': 'Accept-Encoding',
        'Content-Length': len(response.data)
    })


def encode_deflate(fn):
    """
    Deflate(zlib) encoder
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            _zipper = _get_zipper()
            return _zipper._encoder_base(encode='deflate',
                                         compressor=deflate_compress,
                                         error_class=DeflateCompressionError,
                                         request=request,
                                         response=response)

        return fn(*args, **kwargs)
    return wrapper
