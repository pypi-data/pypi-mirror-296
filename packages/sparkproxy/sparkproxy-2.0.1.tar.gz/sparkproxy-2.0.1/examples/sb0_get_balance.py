# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from config import supplier_no, host
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from utils import generate_order_id

# client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), api_version=2, host=host)

with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), api_version=1, host=host)

ret, info = client.get_balance()
pprint(ret)
pprint(info)