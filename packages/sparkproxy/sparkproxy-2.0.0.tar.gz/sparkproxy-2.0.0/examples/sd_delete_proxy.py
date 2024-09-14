# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint
from utils import generate_order_id

from config import secret_key, supplier_no, host
from sparkproxy import Auth
from sparkproxy import SparkProxyClient

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)
# with open("key.pem", 'rb') as pem_file:
#     private_key = pem_file.read()
# client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), api_version=1, host=host)

ret, info = client.delete_proxy(req_order_no=generate_order_id(), instances=["fcb2f4e2a950495c95c77bdbe59643f1"])
pprint(ret)
pprint(info)
