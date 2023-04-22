from . import api
from flask import jsonify, request
from ..common.common import *


@api.route("/test/postRequest", methods=["POST"])
def test_post_request():
    data = request.get_json(force=True)
    name = data.get("name")
    test_int = data.get("test_int")
    test_float = data.get("test_float")
    test_bool = data.get("test_bool")
    return jsonify({"code": 200, "success": True})
