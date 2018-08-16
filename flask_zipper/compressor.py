import gzip
import zlib

import brotli
from flask import current_app


def encode_response_data_with_brotli(response):
    """
    A response compressor uses brotli algorithm

    :param response: Flask response object
    """
    response.data = brotli.compress(
        string=response.data,
        mode=current_app.config['BROTLI_MODE'],
        quality=current_app.config['BROTLI_COMPRESS_LEVEL'],
        lgwin=current_app.config['BROTLI_SLIDING_WINDOW_SIZE'],
        lgblock=current_app.config['BROTLI_MAX_INPUT_BLOCK_SIZE']
    )


def encode_response_data_with_deflate(response):
    """
    A response compressor uses zlib

    :param response: Flask response object
    """
    response.data = zlib.compress(
        response.data,
        current_app.config['DEFLATE_COMPRESS_LEVEL']
    )


def encode_response_data_with_gzip(response):
    """
    A response compressor uses gzip

    :param response: Flask response object
    """
    response.data = gzip.compress(
        data=response.data,
        compresslevel=current_app.config['GZIP_COMPRESS_LEVEL']
    )
