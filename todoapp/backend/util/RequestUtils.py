from flask import request


def get(key):
    """
    get the request body

    :param key: the key of the request body
    :return: value of the key
    """
    try:
        parameter = request.json[key]
    except KeyError:
        parameter = None
    return parameter
