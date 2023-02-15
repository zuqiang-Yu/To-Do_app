from flask import jsonify


def success(data):
    """

    :param data:
    """
    result = {
        "message": "Success",
        "code": 200,
        "data": data
    }

    return jsonify(result)


def fail():
    """

    :param data:
    """
    result = {
        "message": "Fail",
        "code": 400,
        "data": None
    }

    return jsonify(result)
