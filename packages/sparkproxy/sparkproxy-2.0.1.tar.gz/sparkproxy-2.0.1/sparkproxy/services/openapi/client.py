# -*- coding: utf-8 -*-
import time
import uuid

from sparkproxy import config
from sparkproxy import http


class SparkProxyClient(object):
    """资源管理客户端

    使用应用密钥生成资源管理客户端，可以进一步：
    1、部署服务和容器，获得信息
    2、创建网络资源，获得信息

    属性：
        auth: 应用密钥对，Auth对象
        host: API host

    接口：
        get_product_stock(args)
        create_proxy(args)
        renew_proxy(args)
        delete_proxy(stack)
        get_order(stack)
        get_instance(stack)
    """

    def __init__(self, auth, api_version=2, host=None):
        self.auth = auth
        self.api_version = api_version
        if host is None:
            self.host = config.get_default("default_api_host")
        else:
            self.host = host

    def __request_params(self, method, version, args):
        if self.api_version == 1:
            base_params = {
                "method": method,
                "version": version if version is not None else "2024-04-08",
                "reqId": str(uuid.uuid4()),
                "timestamp": int(time.time()),
                "supplierNo": self.auth.get_supplier_no(),
                "sign": "",
                "params": args
            }
            base_params["sign"] = self.auth.token_of_request(base_params)

            return base_params
        else:
            base_params = {"method": method, "version": version if version is not None else "2024-04-08",
                           "reqId": str(uuid.uuid4()), "timestamp": int(time.time()),
                           "supplierNo": self.auth.get_supplier_no(),
                           "params": self.auth.encrypt_request(args)}
            return base_params

    def __post(self, method, data=None, version=None):
        url = '{0}/v{1}/open/api'.format(self.host, self.api_version)
        req = self.__request_params(method, version, data)
        ret, info = http._post(url, req)
        if self.api_version > 1 and ret is not None and 'data' in ret:
            ret['data'] = self.auth.decrypt_response(ret['data'])
        return ret, info

    def get_balance(self):
        """获取账户余额

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回服务组列表[<product1>, <product1>, ...]，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('GetBalance', None)

    def get_product_stock(self, proxy_type, country_code=None, area_code=None, city_code=None):
        """获取商品库存

        列出当前所有在售的商品及其库存信息。

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回服务组列表[<product1>, <product1>, ...]，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('GetProductStock',
                           {"proxyType": proxy_type, "countryCode": country_code, "areaCode": area_code, "cityCode": city_code})

    def create_proxy(self, req_order_no, sku, amount, duration, unit, country_code, area_code, city_code, rules=[]):
        """创建代理实例

        创建新代理实例，返回订单信息

        Args:
            req_order_no(str): 请求方订单ID
            sku(str):  商品ID
            amount(int): IP数量
            duration(int): 必要 时长 0无限制
            unit(int): 单位 1 天;2 周（7天）;3 月(自然月; 4年(自然年365，366）
            country_code(str): 必要,国家代码 3位 iso标准
            area_code(str): 必要,州代码 3位 iso标准
            city_code(str): 必要,城市代码 向我方提取
            rules(list): IP段规则数组
                exclude(bool): False-not in  True-in
                cidr(str): ip段，如 154.111.102.0/24
                count(int): 抽取该规则段数量
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            ResponseInfo    请求的Response信息
        """
        return self.__post('CreateProxy', {"reqOrderNo": req_order_no, "productId": sku, "amount": amount,
                                           "duration": duration, "unit": unit, "countryCode": country_code,
                                           "areaCode": area_code, "cityCode": city_code,
                                           "cidrBlocks": rules})
        # return self.__post('CreateProxy', {"reqOrderNo": req_order_no, "productId": sku, "amount": amount,
        #                                    "duration": duration, "unit": unit, "countryCode": country_code,
        #                                    "cityCode": city_code, "regionId": "", "securityGroupId": "", "imageId": ""})

    def renew_proxy(self, req_order_no, instances):
        """续费代理实例

        续费新代理实例，返回新订单信息

        Args:
            - args:  订单&实例描述

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('RenewProxy', {"reqOrderNo": req_order_no, "instances": instances})
        self._decode_password(ret)
        return ret, info

    def delete_proxy(self, req_order_no, instances):
        """删除代理实例

        删除代理实例，删除即时生效

        Args:
            req_order_no (str):  订单号
            instances (list):
                instanceId (str): 实例ID
                duration (int): 时长
                unit (int): 1-天 2-周 3-月 4-年
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('DelProxy', {"reqOrderNo": req_order_no, "instanceIds": instances})
        self._decode_password(ret)
        return ret, info

    def get_order(self, req_order_no):
        """获取订单信息

        获取订单信息

        Args:
            req_order_no (str):  请求方订单ID

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetOrder', {"reqOrderNo": req_order_no})
        self._decode_password(ret)
        return ret, info

    def _decode_password(self, ret):
        if self.api_version == 1 and ret is not None and 'code' in ret and ret['code'] == 200 and 'data' in ret:
            data = ret['data']
            if 'ipInfo' in data:
                for ipInfo in data['ipInfo']:
                    password = ipInfo["password"] if "password" in ipInfo else ''
                    if len(password) > 0:
                        ipInfo["password"] = self.auth.decrypt_using_private_key(password)

    def get_instance(self, instance_id):
        """获取订单信息

        获取订单信息

        Args:
            instance_id (str):  实例ID

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetInstance', {"instanceId": instance_id})
        if self.api_version == 1:
            if ret is not None and 'code' in ret and ret['code'] == 200 and 'data' in ret:
                data = ret['data']
                password = data["password"] if 'password' in data else ''
                if len(password) > 0:
                    data["password"] = self.auth.decrypt_using_private_key(password)
        return ret, info

    def init_proxy_user(self, user_id, name):
        """获取代理用户

        获取代理用户

        Args:
            user_id (str):  代理账号ID（唯一用户ID）
            name (str):  账号名称

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('InitProxyUser', {"reqUserId": user_id, "name": name})
        return ret, info

    def get_proxy_user(self, username):
        """获取代理用户

        获取代理用户

        Args:
            username (str):  代理账号ID（管理用户）

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetProxyUser', {"reqUserId": username})
        return ret, info

    def recharge_traffic(self, username, req_order_no, traffic, validity_days):
        """流量充值

        Args:
            - username:  流量账号ID
            - req_order_no: 客方订单号
            - traffic: 流量MB
            - validity_days：有效期

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('RechargeTraffic', {"reqUserId": username, "reqOrderNo": req_order_no, "traffic": traffic, "validityDays": validity_days})
        return ret, info

    def get_traffic_record(self, req_order_no):
        """获取流量充值订单信息

        Args:
            - req_order_no: 客方订单号

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetTrafficRecord', {"reqOrderNo": req_order_no})
        return ret, info

    def list_traffic_usages(self, username, start_time, end_time, type):
        """获取流量使用记录

        Args:
            - username:  关联流量账号
            - start_time: 开始时间, 可选参数, ex: 2024-05-01 00:00:00
            - end_time: 结束时间, 可选参数, ex: 2024-07-01 00:00:00
            - type: days / hours

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('ListTrafficUsage', {"reqUserId": username, "startTime": start_time, "endTime": end_time, "type": type})
        return ret, info

    def get_proxy_endpoints(self, country_code):
        """流量充值

        Args:
            country_code (str):  国家代码

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetProxyEndpoints', {"countryCode": country_code})
        return ret, info

    def custom_list_cidr_info(self, cidr='', country_code='', state_code='', city_code='', page=1, pageSize=100):
        """分页获取所有的IP的段

        Args:
            cidr (str): 模糊搜索IP段
            country_code (str):  国家代码
            state_code (str): 省州代码
            city_code (str): 城市代码
            page (int): 页面(从1开始)
            pageSize (int): 每页记录数(100)
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
                data (dict)
                    total (int): 总数
                    page (int): 当前分页
                    list (list): 列表
                        cidr (str): cidr
                        countryName (str): 国家名称
                        stateName (str): 省州名称
                        cityName (str): 城市名称
                        total (int): 总IP数据
                        remains (int): 剩余IP数
                        cooldown (int): 冷却期IP数
                        accounts (int): 正在使用的账户数

            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('CustomQueryAreaCidrList', {
            "cidr": cidr,
            "countryCode": country_code,
            "stateCode": state_code,
            "cityCode": city_code,
            "page": page,
            "pageSize": pageSize
        })
        return ret, info

    def custom_list_cidr_ips(self, cidr='', page=1, pageSize=100):
        """获取IP段下IP列表

        Args:
            cidr (str): IP段
            page (int): 页面(从1开始)
            pageSize (int): 每页记录数(100)
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
                data (dict)
                    total (int): 总数
                    page (int): 当前分页
                    list (list): 列表
                        ip (str): ip
                        countryCode (str): 国家代码
                        countryName (str): 国家名称
                        stateCode (str): 省洲代码
                        stateName (str): 省州名称
                        cityCode (str): 城市代码
                        cityName (str): 城市名称
                        enabled (bool): 是否有效
                        state (int): 状态, 0-free 1-locked 2-used 3-cooldown
                        autoUnlockAt (str): 自动解锁时间
                        accounts (int): 正在使用的账户数
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('CustomListCidrIps', {
            "cidr": cidr,
            "page": page,
            "pageSize": pageSize
        })
        return ret, info

    def custom_create_proxy(self, req_order_no, ips, shareable=True):
        """指定IP创建代理账号

        Args:
            req_order_no (str): 订单号
            ips (list):  ip数组
            shareable (bool): 是否可复用
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('CustomCreateProxy', {
            "reqOrderNo": req_order_no,
            "ips": ips,
            "shareable": shareable
        })
        return ret, info

    def custom_renew_proxy(self, req_order_no, instances):
        """续费代理实例

        续费新代理实例，返回新订单信息

        Args:
            req_order_no (str): 订单ID
            instances (list): 实例信息
                account: ip:port:user:password
                duration: 时长
                unit (int): 1-天 2-周 3-月 4-年

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('CustomRenewProxy', {"reqOrderNo": req_order_no, "instances": instances})
        return ret, info

    def custom_del_proxy(self, reqOrderNo, accounts):
        """ 手动删除代理账号

        Args:
            reqOrderNo (str): 订单ID
            accounts (list):  代理账号列表，格式如：host:port:user:pass

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            result (dict)         成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            ResponseInfo (response)    请求的Response信息
        """
        return self.__post('CustomDelProxy', {"reqOrderNo": reqOrderNo, "accounts": accounts})

    def create_dynamic_user(self, username, password, status):
        """创建动态代理账号

        Args:
            - username:  客方用户ID
            - password: 密码
            - status: 1=状态 2=禁用

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('CreateUser', {"username": username, "password": password, "status": status})

    def update_dynamic_user(self, username, password=None, status=None):
        """更新动态代理账号

        Args:
            - username:  客方用户ID 必填
            - password: 密码 可选
            - status: 1=状态 2=禁用 可选

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('UpdateUser', {"username": username, "password": password, "status": status})

    def get_dynmaic_user_info(self, username):
        """获取动态代理账号

        Args:
            - username:  客方用户ID 必填

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('GetUserInfo', {"username": username})

    def create_dynamic_sub_user(self, main_username, username, password, status, usage_limit, remark):
        """创建动态代理子账号

        Args:
            - main_username 客方主账号  必填
            - username  客方子账号 必填
            - password 代理认证密码 必填
            - status 1-可用 2-禁用
            - usage_limit 可用流量 MB
            - remark 备注
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('CreateSubUser', {"mainUsername": main_username, "username": username, "password": password,
                                             "status": status, "limitFlow": usage_limit, "remark": remark})

    def update_dynamic_sub_user(self, main_username, username, password=None, status=None, usage_limit=None, remark=None):
        """更新动态代理子账号

        Args:
            - main_username 客方主账号  必填
            - username  客方子账号 必填
            - password 代理认证密码 可选
            - status 1-可用 2-禁用 可选
            - usage_limit 可用流量 MB 可选
            - remark 备注 可选
        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('UpdateSubUser', {"mainUsername": main_username, "username": username, "password": password,
                                             "status": status, "limitFlow": usage_limit, "remark": remark})

    def distribute_flow(self, username, req_order_no, flow):
        """分配流量

        Args:
            - username:  流量账号ID
            - req_order_no: 客方订单号
            - traffic: 流量MB

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('DistributeFlow',
                                {"username": username, "reqOrderNo": req_order_no, "flow": flow})
        return ret, info

    def recycle_flow(self, username, req_order_no, flow):
        """回收流量

        Args:
            - username:  流量账号ID
            - req_order_no: 客方订单号
            - traffic: 流量MB

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('RecycleFlow',
                                {"username": username, "reqOrderNo": req_order_no, "flow": flow})
        return ret, info

    def get_dynamic_area(self, proxy_type, product_id):
        """获取动态代理地区

            Args:
                - proxy_type:  代理类型 104
                - product_id: 代理商品SKU

            Returns:
                返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
                - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
                - ResponseInfo    请求的Response信息
            """
        ret, info = self.__post('GetDynamicArea',
                                {"proxyType": proxy_type, "productId": product_id})
        return ret, info

    def draw_dynamic_ips(self, username, region=None, sessTime=5, num=1, format='host:port:user:pass'):
        """获取动态代理地区

            Args:
                - username 子账号 必填
                - region IP区域 不填则全球混播
                - sessTime 会话有效期 默认5分钟
                - num 默认1
                - format 默认 host:port:user:pass

            Returns:
                返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
                - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
                - ResponseInfo    请求的Response信息
            """
        ret, info = self.__post('DrawDynamicIp',
                                {"username": username, "region": region, "sessTime": sessTime, "num": num})
        return ret, info

    def get_flow_use_log(self, username, start_time, end_time, page=1, page_size=100):
        """获取流量使用记录

        Args:
            - username:  关联流量账号
            - start_time: 开始时间, 可选参数, ex: 2024-05-01 00:00:00
            - end_time: 结束时间, 可选参数, ex: 2024-07-01 00:00:00
            - page: 页面，从1开始
            - page_size: 页面大小，默认100

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetFlowUseLog', {"username": username, "startTime": start_time,
                                                  "endTime": end_time, "page": page, "pageSize": page_size})
        return ret, info


