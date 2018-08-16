class ZipperError(Exception):
    """
    Base Exception
    """
    pass


class BrotliCompressionError(ZipperError):
    """
    Brotli Exception
    """
    pass


class GzipCompressionError(ZipperError):
    """
    Gzip Exception
    """
    pass


class DeflateCompressionError(ZipperError):
    """
    Deflate Exception
    """
    pass
