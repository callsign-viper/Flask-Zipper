from brotli import MODE_GENERIC

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
        @app.errorhandler(GzipCompressionError)
        def handle_gzip_compression_error(e):
            pass

        @app.errorhandler(BrotliCompressionError)
        def handle_brotli_compression_error(e):
            pass

        @app.errorhandler(DeflateCompressionError)
        def handle_deflate_compression_error(e):
            pass
