# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from config import supplier_no, host, secret_key
from sparkproxy import Auth
from sparkproxy import SparkProxyClient

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

# with open("key.pem", 'rb') as pem_file:
#     private_key = pem_file.read()
# client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), api_version=1, host=host)


# 获取订单&实例信息
ret, info = client.get_order(req_order_no="17256175319633912")
pprint(ret)
pprint(info)

# 主动获取实例信息
ret, info = client.get_instance(instance_id="fcb2f4e2a950495c95c77bdbe59643f1")
pprint(ret)
pprint(info)

