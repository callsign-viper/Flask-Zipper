import gzip
import zlib

import brotli
from flask import current_app


def encode_response_with_brotli(response):
    response.data = brotli.compress(
        string=response.data,
        mode=current_app.config['BROTLI_MODE'],
        quality=current_app.config['BROTLI_COMPRESS_LEVEL'],
        lgwin=current_app.config['BROTLI_SLIDING_WINDOW_SIZE'],
        lgblock=current_app.config['BROTLI_MAX_INPUT_BLOCK_SIZE']
    )


def encode_response_with_deflate(response):
    response.data = zlib.compress(
        response.data,
        current_app.config['DEFLATE_COMPRESS_LEVEL']
    )


def encode_response_with_gzip(response):
    response.data = gzip.compress(
        data=response.data,
        compresslevel=current_app.config['GZIP_COMPRESS_LEVEL']
    )
