# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint

from config import supplier_no, secret_key, host
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from utils import generate_order_id

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), api_version=2, host=host)

# with open("key.pem", 'rb') as pem_file:
#     private_key = pem_file.read()
# client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), api_version=1, host=host)

ret, info = client.get_product_stock(proxy_type=103)
if ret is not None:
    pprint(ret)
    pprint(info)

    if ret['data'] is not None:
        if 'products' in ret['data'] and len(ret['data']['products']) > 0:
            product = ret['data']['products'][1]
            sku = product["productId"]
        else:   # v1
            product = ret['data'][0]['skus'][1]
            sku = product["sku"]

#         ret, info = client.create_proxy(req_order_no=generate_order_id(), sku=sku, amount=1, duration=product["duration"],
#                                         unit=product["unit"],
#                                         country_code=product["countryCode"], area_code=product["areaCode"], city_code=product["cityCode"])
#         pprint(ret)
#         pprint(info)
#         if ret is not None and ret["code"] == 200:
#             ret, info = client.get_order(ret['data']["reqOrderNo"])
#             pprint(ret)
#             pprint(info)
#
# assert ret is not None