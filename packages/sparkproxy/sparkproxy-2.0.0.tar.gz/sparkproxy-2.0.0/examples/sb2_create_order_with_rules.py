# -*- coding: utf-8 -*-
# flake8: noqa
from pprint import pprint
from utils import generate_order_id
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from config import secret_key, supplier_no, host

client = SparkProxyClient(Auth(supplier_no=supplier_no, secret_key=secret_key), host=host)

ret, info = client.get_product_stock(proxy_type=103)
if ret is not None:
    pprint(ret)

    if ret['data'] is not None and len(ret['data']['products']) > 0:
        product = ret['data']['products'][1]
        cidrBlocks = product['cidrBlocks']

        rules = []

        # CASE-1.1: 从指定IP段抽取指定数量段IP
        if len(cidrBlocks) > 0:
            rules.append({'cidr': cidrBlocks[0]['cidr'], 'count': 2})

        # CASE-1.2: 从指定IP段之外抽取指定数量段IP
        # if len(cidrBlocks) > 0:
        #     rules.append({'exclude': True, 'cidr': cidrBlocks[0]['cidr'], 'count': 2})

        # CASE-1.3: 从指定IP段抽取指定数量段IP, 从指定IP段之外抽取指定数量段IP
        # if len(cidrBlocks) > 1:
        #     rules.append({'exclude': False, 'cidr': cidrBlocks[0]['cidr'], 'count': 1})
        #     rules.append({'exclude': True, 'cidr': cidrBlocks[1]['cidr'], 'count': 1})

        # CASE-2: 从指定IP段抽取指定数量段IP，数量不对： order item quantity is inconsistent with cidr rules
        # if len(cidrBlocks) > 0:
        #     rules.append({'cidr': cidrBlocks[0]['cidr'], 'count': 1})

        # CASE-3.1: 多条相同段规则：cidr blocks is conflict
        # if len(cidrBlocks) > 0:
        #     rules.append({'cidr': cidrBlocks[0]['cidr'], 'count': 1})
        #     rules.append({'cidr': cidrBlocks[0]['cidr'], 'count': 1})

        # CASE-3.2: 排除规则与包含规则冲突：cidr blocks is conflict
        # if len(cidrBlocks) > 0:
        #     rules.append({'cidr': cidrBlocks[0]['cidr'], 'count': 1})
        #     rules.append({'exclude': True, 'cidr': cidrBlocks[0]['cidr'], 'count': 1})

        # CASE-4: IP段不属于该产品：cidr block is invalid or stock is not enough
        # if len(cidrBlocks) > 0:
        #     rules.append({'cidr': "192.168.1.0/24", 'count': 2})

        ret, resp = client.create_proxy(req_order_no=generate_order_id(), sku=product["productId"], amount=2, duration=product["duration"]*2,
                                        unit=product["unit"],
                                        country_code=product["countryCode"], area_code=product["areaCode"], city_code=product["cityCode"],
                                        rules=rules)
        if not ret:
            pprint(resp)
        else:
            pprint(ret)


