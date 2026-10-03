from flask import jsonify


def error(message, status=400, details=None):
    payload = {"error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status


def required(data, fields):
    return [f for f in fields if data.get(f) in (None, "")]
