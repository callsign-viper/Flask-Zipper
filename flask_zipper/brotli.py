from functools import wraps
import brotli
from flask import after_this_request, request, current_app

from .exceptions import BrotliCompressionError


def encode_brotli(fn):
    """
    Brotli encoder
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            if 'br' not in request.headers.get('Accept-Encoding', '')\
                    or not 200 <= response.status_code < 300\
                    or 'Content-Encoding' in response.headers:
                # 1. Accept-Encoding에 br이 포함되어 있지 않거나
                # 2. 200번대의 status code로 response하지 않거나
                # 3. response header에 이미 Content-Encoding이 명시되어 있는 경우
                return response

            try:
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

            except Exception as e:
                raise BrotliCompressionError(e)

            finally:
                return response

        return fn(*args, **kwargs)
    return wrapper
