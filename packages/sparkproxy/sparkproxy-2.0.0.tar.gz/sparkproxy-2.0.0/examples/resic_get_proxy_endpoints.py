# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from config import secret_key, supplier_no, host
from sparkproxy import SparkProxyClient, Auth

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

# 获取订单&实例信息
ret, info = client.get_proxy_endpoints("USA")
pprint(ret)
pprint(info)
