from flask import current_app


def get_zipper():
    try:
        return current_app.extensions['flask-zipper']
    except KeyError:  # pragma: no cover
        raise RuntimeError("You must initialize a Zipper with this flask "
                           "application before using this method")