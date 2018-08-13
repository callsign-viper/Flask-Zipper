from functools import wraps
import gzip
from flask import after_this_request, request, current_app

from .util import _get_zipper
from .exceptions import GzipCompressionError


def gzip_compress(response):
    response.data = gzip.compress(data=response.data,
                                  compresslevel=current_app.config['GZIP_COMPRESS_LEVEL'])
    response.headers.update({
        'Content-Encoding': 'gzip',
        'Vary': 'Accept-Encoding',
        'Content-Length': len(response.data)
    })


def encode_gzipped(fn):
    """
    gzip encoder
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            _zipper = _get_zipper()
            return _zipper._encoder_base(encode="gzip",
                                         compressor=gzip_compress,
                                         error_class=GzipCompressionError,
                                         request=request,
                                         response=response)

        return fn(*args, **kwargs)

    return wrapper
