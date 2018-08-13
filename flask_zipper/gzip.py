from functools import wraps
import gzip
from flask import after_this_request, request, current_app

from .exceptions import GzipCompressionError


def encode_gzipped(fn):
    """
    gzip encoder
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            if 'gzip' not in request.headers.get('Accept-Encoding', '') \
                    or not 200 <= response.status_code < 300 \
                    or 'Content-Encoding' in response.headers:
                # 1. Accept-Encoding에 gzip이 포함되어 있지 않거나
                # 2. 200번대의 status code로 response하지 않거나
                # 3. response header에 이미 Content-Encoding이 명시되어 있는 경우
                return response

            try:
                response.data = gzip.compress(data=response.data,
                                              compresslevel=current_app.config['GZIP_COMPRESS_LEVEL'])
                response.headers.update({
                    'Content-Encoding': 'gzip',
                    'Vary': 'Accept-Encoding',
                    'Content-Length': len(response.data)
                })

            except Exception as e:
                raise GzipCompressionError(e)

            finally:
                return response

        return fn(*args, **kwargs)

    return wrapper
