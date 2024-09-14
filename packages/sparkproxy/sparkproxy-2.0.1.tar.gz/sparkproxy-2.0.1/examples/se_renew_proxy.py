# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from config import secret_key, supplier_no, host
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from utils import generate_order_id

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

# with open("key.pem", 'rb') as pem_file:
#     private_key = pem_file.read()
# client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), api_version=1, host=host)


# # 已生效、未过期的实例，可以续费
# ret, info = client.renew_proxy(req_order_no=generate_order_id(), instances=[
#     {"instanceId": "f2d8469daf5b4a9abe1a359b950d7608", "duration": 30, "unit": 1}])
# pprint(ret)
# pprint(info)


# # 冷却期的IP，过期的共享代理，可以续费
# ret, info = client.renew_proxy(req_order_no=generate_order_id(), instances=[
#     {"instanceId": "63642b8c2ec7483598b10cb4835ce8af", "duration": 30, "unit": 1}])
# pprint(ret)
# pprint(info)


# # 冷却期的IP，过期的独享代理，可以续费
# ret, info = client.renew_proxy(req_order_no=generate_order_id(), instances=[
#     {"instanceId": "152137d4b67a4ac19932a23cd2d4f6ad", "duration": 30, "unit": 1}])
# pprint(ret)
# pprint(info)

# 按上次的时长续费
ret, info = client.renew_proxy(req_order_no=generate_order_id(), instances=[
    {"instanceId": "fcb2f4e2a950495c95c77bdbe59643f1", "duration": 30, "unit": 1}])
pprint(ret)
pprint(info)