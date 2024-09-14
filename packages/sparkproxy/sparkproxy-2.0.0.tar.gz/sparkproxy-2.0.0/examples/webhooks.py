# -*- coding: utf-8 -*-
import os
from pprint import pprint

from flask import Flask, request

from config import secret_key, supplier_no, host
from sparkproxy import Auth, SparkProxyClient

auth = Auth(supplier_no=supplier_no, secret_key=secret_key)
client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)


def verify_request(req):
    if req.is_json:
        params = req.json

        try:
            params['data'] = auth.decrypt_response(params['data'])
        except ValueError:
            return "Bad signature", 400
    else:
        return "Bad request", 400

    return None, 200


app = Flask(__name__)


@app.route("/product/sync", methods=["POST"])
def receiveSyncProducts():
    ret, code = verify_request(request)
    if ret is not None:
        return {"code": 400, "msg": "签名校验失败"}

    ret = request.json
    pprint(ret)

    return {"code": 200, "msg": "ok"}


@app.route("/instance/sync", methods=["POST"])
def receiveSyncInstances():
    ret, code = verify_request(request)
    if ret is not None:
        return {"code": 400, "msg": "签名校验失败"}

    ret = request.json
    pprint(ret)

    return "", 200


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
