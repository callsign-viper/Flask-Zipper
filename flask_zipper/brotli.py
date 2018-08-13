from functools import wraps
import brotli
from flask import after_this_request, request, current_app

from .exceptions import BrotliCompressionError
from .util import _get_zipper

def brotli_compress(response):
    response.data = brotli.compress(string=response.data,
                                    mode=current_app.config['BROTLI_MODE'],
                                    quality=current_app.config['BROTLI_COMPRESS_LEVEL'],
                                    lgwin=current_app.config['BROTLI_SLIDING_WINDOW_SIZE'],
                                    lgblock=current_app.config['BROTLI_MAX_INPUT_BLOCK_SIZE'])
    response.headers.update({
        'Content-Encoding': 'br',
        'Vary': 'Accept-Encoding',
        'Content-Length': len(response.data)
    })

def encode_brotli(fn):
    """
    Brotli encoder
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            _zipper = _get_zipper()
            return _zipper._encoder_base(encode='br',
                                         compressor=brotli_compress,
                                         error_class=BrotliCompressionError,
                                         request=request,
                                         response=response)

        return fn(*args, **kwargs)
    return wrapper
