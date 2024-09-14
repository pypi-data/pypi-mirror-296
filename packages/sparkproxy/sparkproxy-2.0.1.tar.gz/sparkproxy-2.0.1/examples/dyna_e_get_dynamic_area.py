# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from config import secret_key, supplier_no, host
from sparkproxy import SparkProxyClient, Auth
from utils import generate_order_id

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

order_no = generate_order_id()
ret, info = client.get_dynamic_area(proxy_type=104, product_id="")
pprint(ret)
pprint(info)