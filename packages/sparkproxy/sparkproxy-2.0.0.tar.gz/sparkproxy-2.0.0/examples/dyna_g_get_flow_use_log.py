# -*- coding: utf-8 -*-
# flake8: noqa
from config import secret_key, supplier_no, host
from sparkproxy import SparkProxyClient, Auth

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

ret, info = client.get_flow_use_log(username="yd_200005", start_time="2024-07-08 23:59:59", end_time="2024-08-28 23:59:59", page=1, page_size=100)
print(ret)
print(info)