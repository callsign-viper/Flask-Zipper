class ZipperError(Exception):
    pass


class BrotliCompressionError(ZipperError):
    pass


class GzipCompressionError(ZipperError):
    pass


class DeflateCompressionError(ZipperError):
    pass
