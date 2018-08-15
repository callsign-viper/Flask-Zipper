from functools import wraps

from flask import after_this_request, request

from flask_zipper.compressor import *
from flask_zipper.exceptions import *
from flask_zipper.util import get_zipper


def encode_brotli(fn):
    """
    Brotli encoder
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            return get_zipper().encode_response(
                encode='br',
                compressor=encode_response_with_brotli,
                error_class=BrotliCompressionError,
                response=response
            )

        return fn(*args, **kwargs)
    return wrapper


def encode_deflate(fn):
    """
    Deflate(zlib) encoder
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            return get_zipper().encode_response(
                encode='deflate',
                compressor=encode_response_with_deflate,
                error_class=DeflateCompressionError,
                response=response
            )

        return fn(*args, **kwargs)
    return wrapper


def encode_gzipped(fn):
    """
    gzip encoder
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            return get_zipper().encode_response(
                encode='gzip',
                compressor=encode_response_with_gzip,
                error_class=GzipCompressionError,
                response=response
            )

        return fn(*args, **kwargs)

    return wrapper
