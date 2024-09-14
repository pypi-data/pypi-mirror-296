# -*- coding: utf-8 -*-
# flake8: noqa

from pprint import pprint

from config import secret_key, supplier_no, host
from sparkproxy import Auth
from sparkproxy import SparkProxyClient

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

# 更新代理子账号
main_username = "yd_200005"   # 客户方唯一用户ID
username = "yd_200005_03"   # 客户方唯一用户ID
password = "1234"
usage_limit = 5  # MB
status = 1  # 1-可用 2-禁用
remark = '测试用户1'

# Case-1: 正常
ret, info = client.update_dynamic_sub_user(main_username=main_username, username=username, password=password,
                                        status=status, usage_limit=usage_limit, remark=remark)
pprint(ret)
pprint(info)

# Case-2: 启用/停用
ret, info = client.update_dynamic_sub_user(main_username=main_username, username=username, status=status)
pprint(ret)
pprint(info)