# -*- coding: utf-8 -*-
# flake8: noqa

from pprint import pprint

from config import secret_key, supplier_no, host
from sparkproxy import Auth
from sparkproxy import SparkProxyClient

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

# 创建代理账号
username = "yd_200005"   # 客户方唯一用户ID
password = "1234"
status = 1

# 修改密码
ret, info = client.update_dynamic_user(username=username, password=password)
pprint(ret)
pprint(info)

# 修改状态
ret, info = client.update_dynamic_user(username=username, status=status)
pprint(ret)
pprint(info)