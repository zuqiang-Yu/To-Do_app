from flask import jsonify


def success(data=None):
    """

    :param data:
    """
    if data is not None:

      result = {
          "message": "Success",
          "code": 200,
          "data": data
      }
    else:
      result = {
        "message": "Success",
        "code": 200
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
