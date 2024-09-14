# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from config import secret_key, supplier_no, host
from sparkproxy import Auth
from sparkproxy import SparkProxyClient

# client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), api_version=1, host=host)

ret, info = client.get_product_stock(proxy_type=103)
if ret is not None and ret['code'] == 200:
    pprint(ret)
    pprint(info)
    assert ret['data']['page'] > 0
    assert ret['data']['total'] > 0
    assert len(ret['data']['products'][0]['countryCode']) > 0
else:
    pprint(info)