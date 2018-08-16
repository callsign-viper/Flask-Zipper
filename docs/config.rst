.. _Configuration Options:

Configuration Options
=====================

You can change many options for how this extension works via

.. code-block:: python

  app.config[OPTION_NAME] = new_options

Gzip Compressing Options
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{6cm}|p{7cm}|

=================================== =========================================
``GZIP_COMPRESS_LEVEL``             default is 9
=================================== =========================================

Brotli Compressing Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{6cm}|p{7cm}|

=================================== =========================================
``BROTLI_QUALITY_LEVEL``            default is 11
``BROTLI_MODE``                     default is `MODE_GENERIC`
``BROTLI_SLIDING_WINDOW_SIZE``      default is 22
``BROTLI_MAX_INPUT_BLOCK_SIZE``     default is 0
=================================== =========================================

Deflate Compressing Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{6cm}|p{7cm}|

=================================== =========================================
``DEFLATE_COMPRESS_LEVEL``          default is 9
=================================== =========================================