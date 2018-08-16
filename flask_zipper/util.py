from flask import current_app


def get_zipper():
    """
    A function to get current :class Zipper: extension from context
    :return: Zipper
    """
    try:
        return current_app.extensions['flask-zipper']
    except KeyError:  # pragma: no cover
        raise RuntimeError("You must initialize a Zipper with this flask "
                           "application before using this method")
