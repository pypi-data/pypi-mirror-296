# -*- coding: utf-8 -*-
# flake8: noqa

from pprint import pprint

from config import secret_key, supplier_no, host
from sparkproxy import Auth
from sparkproxy import SparkProxyClient

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

# 创建代理账号
username = "yd_200005"   # 客户方唯一用户ID

# 获取用户信息
ret, info = client.get_dynamic_user_info(username=username)
pprint(ret)
pprint(info)