from brotli import MODE_GENERIC
from flask import request

from .exceptions import *


class Zipper(object):
    """
    An object used to hold compressor settings for the
    Flask-Zipper extension.
    Instances of :class:`Zipper` are *not* bound to specific apps, so
    you can create one in the main body of your code and then bind it
    to your app in a factory function.
    """

    def __init__(self, app=None):
        """
        Create the Flask-Zipper instance. You can either pass a flask application in directly
        here to register this extension with the flask app, or call init_app after creating
        this object (in a factory pattern).
        :param app: A flask application
        """
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Register this extension with the flask app.
        :param app: A flask application
        """
        # Save this so we can use it later in the extension
        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}
        app.extensions['flask-zipper'] = self

        self._set_default_configuration_options(app)
        self._set_default_errorhandler(app)

    @staticmethod
    def _set_default_configuration_options(app):
        """
        Sets the default configuration options used by this extension
        """

        # gzip config
        app.config.setdefault('GZIP_COMPRESS_LEVEL', 9)

        # brotli config
        app.config.setdefault('BROTLI_QUALITY_LEVEL', 11)
        app.config.setdefault('BROTLI_MODE', MODE_GENERIC)
        app.config.setdefault('BROTLI_SLIDING_WINDOW_SIZE', 22)
        app.config.setdefault('BROTLI_MAX_INPUT_BLOCK_SIZE', 0)

        # deflate(zlib) config
        app.config.setdefault('DEFLATE_COMPRESS_LEVEL', 9)

    @staticmethod
    def _set_default_errorhandler(app):
        """
        Sets the default error handler used by this extension
        """
        @app.errorhandler(GzipCompressionError)
        def handle_gzip_compression_error(e):
            pass

        @app.errorhandler(BrotliCompressionError)
        def handle_brotli_compression_error(e):
            pass

        @app.errorhandler(DeflateCompressionError)
        def handle_deflate_compression_error(e):
            pass

    def encode_response(self, content_encoding_string: str, compress_function, error_class: Exception, response):
        """
        A encoder to compress response with delivered compressor and other arguments

        :param content_encoding_string: Content-Encoding argument like `br`, 'deflate', `gzip`
        :param compress_function: Compressor in :mod:`flask_zipper.compressor`
        :param error_class: Exception in :mod:`flask_zipper.exceptions`
        :param response: Response object to compress
        :return: Compressed response
        """
        if content_encoding_string.upper() not in request.headers.get('Accept-Encoding', '').upper() \
                or 'Content-Encoding' in response.headers \
                or not 200 <= response.status_code < 300 \
                or response.direct_passthrough:
            # 1. Accept-Encoding에 encode가 포함되어 있지 않거나
            # 2. 200번대의 status code로 response하지 않거나
            # 3. response header에 이미 Content-Encoding이 명시되어 있거나
            # 4. direct passthrough거나
            return response

        try:
            compress_function(response)
            response.headers.extend({
                'Content-Encoding': content_encoding_string,
                'Vary': 'Accept-Encoding',
                'Content-Length': len(response.data)
            })

        except Exception as e:
            raise error_class(e)

        finally:
            return response
