# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from config import secret_key, supplier_no, host
from sparkproxy import SparkProxyClient, Auth

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

username = "yd_200005_03"
region="us"
sessTime=None
num=1
ret, info = client.draw_dynamic_ips(username=username, region=region, sessTime=sessTime, num=num)
pprint(ret)
pprint(info)